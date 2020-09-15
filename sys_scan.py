import os
import sys
import csv
import json

from classes.detection import Detection
import utils.csv_helper as csv_helper

from requests_html import HTMLSession

# Constants
PRINT_DEBUG = True # False to turn debug prints off
MODEL_CSV_FILENAME = 'model.csv'
AVAILABLE_TOOLS = ['anchore', 'zap', 'joomscan']
CVE_BASE_PATH = 'https://cve.mitre.org/cgi-bin/cvename.cgi?name='

# Custom functions
def retrieveCWEURLFromCVE(cve_full_url=None, cve_id=None):
    """
    Please specify either cve_full_url OR cve_id
    Priority non-null arg: cve_full_url

    Examples:
    cve_full_url=https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-7589
    OR
    cve_id=CVE-2015-7589
    """

    if (not cve_full_url is None) and (not cve_full_url.startswith('https://cve.mitre.org/')):
        raise ValueError('Invalid CVE url')

    if (cve_full_url is None) and (cve_id is None):
        return None

    url = ''

    if not (cve_full_url is None):
        url = cve_full_url
        cve_regex_test = re.search("CVE-[0-9]+-[0-9]+", url)
        if cve_regex_test:
            cve_id = cve_regex_test.group()
        else:
            cve_id = url
    else:
        url = CVE_BASE_PATH + cve_id

    print("[retrieveCWEURLFromCVE] Parsing CVE: " + cve_id + ", from url: " + url)

    cve_response = HTMLSession().get(url).html
    cve_url = cve_response.find("div#GeneratedTable .ltgreybackground .larger a", first=True).attrs['href']
    cve_response = session.get(cve_url).html
    
    if not cve_response.find("div#vulnTechnicalDetailsDiv td a", first=True) is None:
        cwe_url = cve_response.find("div#vulnTechnicalDetailsDiv td a", first=True).attrs['href']
    else:
        cwe_url = ''

    if PRINT_DEBUG is True:
        print("[retrieveCWEURLFromCVE] CWE Url of " + cve_id + ": " + cwe_url)

    return cwe_url

# Parsing input parameters
IMAGE_NAME = ''
IMAGE_TAG = ''
APP_URI = ''

if (len(sys.argv)<6) or ( '--help' == str(sys.argv[1]).lower() ) :
    print('Usage: sys_scan.py app_name app_version commit_id image_name image_tag app_uri [tool1 tool2 ... toolN]')
    print('Available tools: ' + str(AVAILABLE_TOOLS) )
    exit(0)

if len(sys.argv)<7:
    raise ValueError('Usage: sys_scan.py app_name app_version commit_id image_name image_tag app_uri [tool1 tool2 ... toolN]')

IMAGE_NAME = str(sys.argv[4])
IMAGE_TAG = str(sys.argv[5])
APP_URI = str(sys.argv[6])

REQUESTED_TOOLS = []
for tool in sys.argv[7:]:
    REQUESTED_TOOLS.append( str(tool).lower() )
    
###

# Initialize model.csv with heading row
csv_helper.initModelWithHeadingRow()

session = HTMLSession()

# Anchore Container Analysis
if 'anchore' in REQUESTED_TOOLS:
    os.system('curl -s https://ci-tools.anchore.io/inline_scan-latest | bash -s -- -p -r '+IMAGE_NAME+':'+IMAGE_TAG)
    with open('./anchore-reports/'+IMAGE_NAME+'_'+IMAGE_TAG+"-vuln.json", encoding='utf-8') as f:
        result_dict = json.load(f)

        with open(MODEL_CSV_FILENAME, 'a') as csv_model:

            csv_model_writer = csv.writer(csv_model)

            vulns = result_dict["vulnerabilities"]

            for vuln in vulns:

                # Get Weakeness details from cwe.mitre.org
                cve_url = vuln["url"]

                url = retrieveCWEURLFromCVE(cve_id=vuln["vuln"])

                if (url is None) or (url == ''):
                    continue

                curr_detection = Detection(
                                            url,
                                            vuln["severity"], 
                                            None, 
                                            vuln["vuln"],
                                            None,
                                            vuln["package"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            'Anchore'
                                            )

                csv_helper.writeRow(csv_model_writer, curr_detection)

# OWAS ZAP
if 'zap' in REQUESTED_TOOLS:
    os.system('docker run -v $(pwd):/zap/wrk/:rw --net="host" -i owasp/zap2docker-stable zap-full-scan.py -g gen.conf -J zap-result.json -m 1 -r zap-result.html -j -a -t ' + APP_URI)

    with open('zap-result.json', encoding='utf-8') as f:
        result_dict = json.load(f)

        with open(MODEL_CSV_FILENAME, 'a') as csv_model:

            csv_model_writer = csv.writer(csv_model)

            for site in result_dict["site"]:
                for alert in site["alerts"]:
                    if int(alert["riskcode"]) > 0 :

                        # Get Weakeness details from cwe.mitre.org
                        url = 'https://cwe.mitre.org/data/definitions/' + alert['cweid'] + '.html'

                        for instance in alert["instances"]:
                            curr_detection = Detection(
                                            url,
                                            alert["riskdesc"][0:alert["riskdesc"].index('(')],
                                            None,
                                            alert["name"],
                                            None,
                                            instance["method"] + ' ' + instance["uri"],
                                            None,
                                            alert["solution"],
                                            None,
                                            None,
                                            'ZAP'
                                            )

                            csv_helper.writeRow(csv_model_writer, curr_detection)

if 'joomscan' in REQUESTED_TOOLS:
    os.system('perl joomscan.pl -u ' + APP_URI + ' > joomscan_result.txt')
    with open('joomscan_result.txt', encoding='utf-8') as f:
        lines = f.readlines()

        with open(MODEL_CSV_FILENAME, 'a') as csv_model:
            csv_model_writer = csv.writer(csv_model)

            i = 0
            for line in lines:

                line = str( bytes(line, 'utf-8').decode('utf-8', 'ignore') )

                if line.startswith('CVE : '):

                    cve_id = line.split(' : ')[1][0:-1]

                    try:
                        if lines[i-1].index('[++] ') > 0:
                            vulnerability_name = str(lines[i-1][lines[i-1].index('[++] ')+5:-1])
                        else:
                            vulnerability_name = lines[i-1][0:-1]
                    except:
                        vulnerability_name = lines[i-1][0:-1]

                    attacks = None
                    for offset in range(1,4) :
                        if lines[i+offset].startswith('EDB : '):
                            attack_url = lines[i+offset].split(' : ')[1][0:-1]
                            attack_url_response = session.get(attack_url).html
                            attacks = attack_url_response.find('h1.card-title', first=True).text

                            if PRINT_DEBUG == True:
                                print('Attack: ' + attacks)
                            break

                    cwe_url = retrieveCWEURLFromCVE(cve_id=cve_id)

                    curr_detection = Detection(
                                                cwe_url,
                                                None,
                                                None,
                                                vulnerability_name + ' (' + cve_id + ')',
                                                None,
                                                APP_URI,
                                                None,
                                                None,
                                                attacks,
                                                None,
                                                'joomscan'
                                                )

                    csv_helper.writeRow(csv_model_writer, curr_detection)

                    if PRINT_DEBUG == True:
                        print()

                i = i + 1