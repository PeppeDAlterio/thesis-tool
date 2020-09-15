import csv
import os
import re

from requests_html import HTMLSession

from classes.detection import Detection

# False to turn debug prints off
PRINT_DEBUG = True

# Initialize Dictionary with CWE-NIST800_53 mapping
cwe_nist_dict = dict()
if os.path.exists('utils/cwe-nist.csv'):
    with open('utils/cwe-nist.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            try:
                nist_id = str(row['NIST-ID'])
            except:
                nist_id = ''
            cwe_nist_dict[ str(row['CWE-ID']) ] = nist_id
else:
    print('WARNING: NO "cwe-nist.csv" mapping file found!')

###

session = HTMLSession()

def initModelWithHeadingRow():
    with open('model.csv', 'w') as f:
        csv_model_writer = csv.writer(f)
        head_row = [
                'Risk', 
                'Threat', 
                'Vulnerability', 
                'Weakness', 
                'Instance',
                'Asset', 
                'Countermeasure', 
                'Attack', 
                'Likelihood Of Exploit', 
                'Scan tool',
                'NIST',
                'Id'
            ]
        csv_model_writer.writerow(head_row)
###

def writeRow(csv_model_writer=None, mDetection=None):
    """
    Writes a new row in csv model.

    Parameters:
        csv_model_writer, current csv writer
        mDetection, object of Detection class

    Returns:

   """

    if (mDetection is None) or (mDetection.__class__.__name__ != Detection.__name__):
        raise ValueError('Invalid mDetection object')

    if (csv_model_writer is None):
        raise ValueError('url and csv_model_write cannot be None')

    response = session.get(mDetection.url).html

    # BEGIN OF RISK
    if(mDetection.risk is None):
        risk_div = response.find("div#Likelihood_Of_Exploit .detail", first=True)
        if risk_div is not None:
            mDetection.risk = response.find("div#Likelihood_Of_Exploit .detail", first=True).text
        else:
            mDetection.risk = 'Unknown'
    
    if PRINT_DEBUG == True:
        print("Risk: " + mDetection.risk)
        print()

    curr_row = [mDetection.risk]

    # END OF RISK

    #
    #

    # BEGIN OF THREAT
    if(mDetection.threats is None):
        mDetection.threats = ''
        consequences_table = response.find("div#Common_Consequences table", first=True)
        if consequences_table is not None:
            consequences_rows = consequences_table.find('tr')
            for row in consequences_rows[1:]:
                curr_threat = row.find('td .smaller i', first=True).text
                for curr_threat in curr_threat.split('; '):
                    if curr_threat.lower().startswith('other'):
                        continue
                    elif curr_threat not in mDetection.threats:
                        mDetection.threats += curr_threat + '; '
            mDetection.threats = mDetection.threats[0:-2]
    
    if PRINT_DEBUG == True:
        print('*** Threat ***')
        print(mDetection.threats)
        print()

    curr_row.append(mDetection.threats)

    # END OF THREAT

    #
    #

    # BEGIN OF VULNERABILITY

    if(mDetection.vulnerability is None):
        # TODO
        pass

    if PRINT_DEBUG == True:
        print("*** Vulnerability ***")
        print(mDetection.vulnerability)
        print()

    curr_row.append(mDetection.vulnerability)

    # END OF VULNERABILITY

    #
    #

    # BEGIN OF WEAKNESS
    if PRINT_DEBUG == True:
        print("*** Weakness ***")

    if(mDetection.weakness is None):

        mDetection.weakness = response.find("td#Contentpane h2", first=True).text + '. '

        if PRINT_DEBUG == True:
            print(response.find("td#Contentpane h2", first=True).text)

        weakeness_description = response.find("div#Description .indent", first=True)

        if weakeness_description is not None:

            if PRINT_DEBUG == True:
                print(weakeness_description.text)

            mDetection.weakness += weakeness_description.text

    if PRINT_DEBUG == True:
        print()

    curr_row.append(mDetection.weakness)

    # END OF WEAKNESS

    #
    #

    # BEGIN OF INSTANCE
    if(mDetection.instance is None):
        # TODO
        pass

    if PRINT_DEBUG == True:
        print("*** Instance ***")
        print(mDetection.instance)
        print()

    curr_row.append(mDetection.instance)

    # END OF INSTANCE

    #
    #

    # BEGIN OF ASSET
    if(mDetection.assets is None):
        mDetection.assets = ''
        consequences_table = response.find("div#Common_Consequences table", first=True)
        if consequences_table is not None:
            consequences_rows = consequences_table.find('tr')
            for row in consequences_rows[1:]:
                curr_assets = row.find('td', first=True).text
                for curr_asset in curr_assets.split('\n'):
                    if curr_asset.lower().startswith('other'):
                        continue
                    elif curr_asset not in mDetection.assets:
                        mDetection.assets += curr_asset + '; '
            mDetection.assets = mDetection.assets[0:-2]

    if PRINT_DEBUG == True:
        print("*** Assets ***")
        print(mDetection.assets)
        print()

    curr_row.append(mDetection.assets)

    # END OF ASSET

    #
    #

    # BEGIN OF COUNTERMEASURE
    # Mitigations
    if(mDetection.countermeasure is None):
        mDetection.countermeasure = ''
        countermeasure_indent = response.find("div#Potential_Mitigations table td", first=True)
        if countermeasure_indent is not None:
            mDetection.countermeasure = countermeasure_indent.text

    if PRINT_DEBUG == True:
        print("*** Countermeasure ***")
        print(mDetection.countermeasure)
        print()

    curr_row.append(mDetection.countermeasure)

    # END OF COUNTERMEASURE

    #
    #

    # BEGIN OF ATTACK
    if(mDetection.attacks is None):
        mDetection.attacks = ''
        attacks_table = response.find("div#Related_Attack_Patterns table", first=True)
        if attacks_table is not None:
            attacks_rows = attacks_table.find('tr')
            for row in attacks_rows[1:]:
                curr_attack = row.find('td')[1].text
                mDetection.attacks += curr_attack + '; '
            mDetection.attacks = mDetection.attacks[0:-2]

    if PRINT_DEBUG == True:
        print('*** Attacks ***')
        print(mDetection.attacks)
        print()

    curr_row.append(mDetection.attacks)

    # END OF ATTACK

    #
    #

    # BEGIN OF LIKELIHOOD OF EXPLOIT
    if(mDetection.likelihood_of_exploit is None):
        likelihood_of_exploit_div = response.find("div#Likelihood_Of_Exploit .detail", first=True)
        if likelihood_of_exploit_div is not None:
            mDetection.likelihood_of_exploit = response.find("div#Likelihood_Of_Exploit .detail", first=True).text
        else:
            mDetection.likelihood_of_exploit = 'Unknown'

    if PRINT_DEBUG == True:
        print('*** Likelihood of Exploit ***')
        print(mDetection.likelihood_of_exploit)
        print()

    curr_row.append(mDetection.likelihood_of_exploit)

    # END OF LIKELIHOOD OF EXPLOIT

    #
    #

    # BEGIN OF SCAN TOOL
    curr_row.append(str(mDetection.scan_tool))
    # END OF SCAN TOOL

    #
    #

    # BEGIF OF NIST
    mDetection.nist = ''
    result = re.search(r'CWE-[0-9]+', mDetection.weakness)
    if result:
      cwe_id = str(result.group().split('-')[1])
      if (cwe_id in cwe_nist_dict):
          mDetection.nist = str( cwe_nist_dict[cwe_id] )

    
    curr_row.append(str(mDetection.nist))
    # END OF NIST

    #
    #

    # BEGIN OF ID
    curr_row.append(str(mDetection.getId()))
    # END OF ID

    #

    if PRINT_DEBUG == True:
        print()
        print('-----')
        print()

    csv_model_writer.writerow( curr_row )