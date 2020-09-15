# ######################### #
# ARGV:                     #
# [0] test_and_report.py    #
# [1] Application name      #
# [2] Application version   #
# [3] Analyzed commit id    #
# ######################### #

import re
import sys
import csv
import os

import utils.parse_case_to_test as parse_case_to_test
import utils.history as history

from datetime import datetime
from os import path

from utils.html_util import report_head_html as report_head

REPORT_FILE_NAME = 'report.html'

def intersection(lst1, lst2): 
  """
  Description
  """
  lst3 = [value for value in lst1 if value in lst2] 
  return lst3

def buildCaseRowHTML(test_case_result, 
    risk,
    vulnerability,
    weakness,
    threat,
    instance,
    asset,
    countermeasure,
    attack,
    likelihood_of_exploit,
    scan_tool,
    id,
    nist,
    regression_collection):
    """
    Description here
    """

    if test_case_result == True:
        curr_html = '<tr height="24" class="test-pass">'
    elif test_case_result == False:
        curr_html = '<tr height="24" class="test-fail">'          
    else:
        curr_html = '<tr height="24" class="test-unknown">'

    curr_html += """
    <th width="20%"><a name="medium"></a>
    """ + risk + """
    </th><th width="80%">
    """ + vulnerability + """
    </th>
    </tr>
    
    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Weakness</td><td width="80%">
    <p>
    """ + weakness + """
    </p>
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Threat</td><td width="80%">
    """ + threat + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Instance</td><td width="80%">
    """ + instance + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Asset</td><td width="80%">
    """ + asset + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Countermeasure</td><td width="80%">
    """ + countermeasure + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Attack</td><td width="80%">
    """ + attack + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Likelihood Of Exploit</td><td width="80%">
    """ + likelihood_of_exploit + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Scan tool</td>
    <td width="80%">
    """ + scan_tool + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Test result</td>
    <td width="80%">
    """

    if test_case_result == True:
        curr_html += '<p style="color: green;"><b>PASS</b></p>'
    elif test_case_result == False:
        curr_html += '<p style="color: red;"><b>FAIL</b></p>'            
    else:
        curr_html += '<p style="color: orange;"><b>UNKNOWN</b></p>' 

    curr_html += """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">Timestamp</td>
    <td width="80%">
    """ + datetime.now().strftime("%d/%m/%Y %H:%M UTC") + """
    </td>
    </tr>

    """ + """
    <tr bgcolor="#e8e8e8">
    <td width="20%">ID</td>
    <td width="80%">
    """ + id + """
    </td>
    </tr>
    
    """ 

    if id in regression_collection:
        curr_html += """
        <tr style="background-color: black; color: white;">
        <td width="20%">Regression</td>
        <td width="80%">
        """ + fix_dict[str(id)] + """
        </td>
        </tr>
        """

    curr_html += """
    <tr bgcolor="#e8e8e8">
    <td width="20%">NIST Security Control</td>
    <td width="80%">
    """ + str( nist ) + """
    </td>
    </tr>
    """
    
    curr_html += """
    <tr>
    <td colspan="2"><div class="spacer"></div></td>
    </tr>
    """

    return curr_html

def buildStatsTableHTML(stats_risk_dict, nist_fail_set):
  """
  """

  if stats_risk_dict is None or len(stats_risk_dict) == 0:
    return

  stats_table_html = """
  <table class="tg">
  <thead>
    <tr>
      <th class="tg-amwm">Risk</th>
      <th class="tg-amwm">Number of occurrences</th>
    </tr>
  </thead>
  <tbody>

  """

  total = 0
  for key in stats_risk_dict:
    stats_table_html += """
    <tr>
      <td class="tg-baqh">""" + key + """</td>
      <td class="tg-baqh">""" + str(stats_risk_dict[key]) + """</td>
    </tr>

    """
    total = total + stats_risk_dict[key]
  
  stats_table_html += """
    <tr>
      <td class="tg-l2oz">Total:</td>
      <td class="tg-baqh">""" + str(total) + """</td>
    </tr>
  </tbody>
  </table>

  """

  stats_table_html += """
  <div class="spacer"></div>

  """

  # Strinfigy nist set
  nist_failing_str = ''
  if not (nist_fail_set is None):
    for e in nist_fail_set:
      nist_failing_str += e + ', '
    if len(nist_failing_str)>0:
      nist_failing_str = nist_failing_str[0:-2]

  stats_table_html += """
  <table class="tg">
  <thead>
    <tr>
      <th class="tg-amwm">Failing NIST Security Controls</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="tg-baqh">""" + nist_failing_str + """</td>
    </tr>
  </tbody>
  </table>
  """

  filedata = ''
  with open(REPORT_FILE_NAME, 'r') as file :
    filedata = file.read()

  filedata = filedata.replace('$PLACE_STATS_TABLE_HERE$', stats_table_html)

  # Write the file out again
  with open(REPORT_FILE_NAME, 'w') as file:
    file.write(filedata)

### APPLICATION DETAIL FROM ARGV ###
app_name = 'APP NAME'
app_version = 'unknown'
app_commit_id = 'unknown_commit'
if len(sys.argv)>1:
  app_name = str(sys.argv[1]).strip()
  if len(sys.argv)>2:
    app_version = str(sys.argv[2]).strip()
    if len(sys.argv)>3:
      app_commit_id = str(sys.argv[3]).strip()

if app_version == '':
  app_version = 'unknown'

if app_commit_id == '':
  app_commit_id = 'unknown'


### REPORT HEAD USING APPLICATION DETAIL ###
report_head = report_head.replace('$app_name$', app_name)
report_head = report_head.replace('$app_version$', app_version)
report_head = report_head.replace('$app_commit_id$', app_commit_id)

### CWE-NIST MAPPING DICTIONARY ###
cwe_nist_dict = dict()
if path.exists('cwe-nist.csv'):
  with open('cwe-nist.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
      try:
        nist_id = str(row['NIST-ID'])
      except:
        nist_id = ''
      cwe_nist_dict[ str(row['CWE-ID']) ] = nist_id

# NIST Failing checks set
nist_fail_set = set()


### HISTORY AND REGRESSION UTILITY DATA STRUCTURES ###
# Detections' IDs from latest model
last_model_ids = []
# Detections' IDs from current model
curr_model_ids = []
# Fix IDs
fixed_ids = []

if path.exists('last-model.csv'):
    with open('last-model.csv', 'r') as old_model_file:
        old_model_reader = csv.DictReader(old_model_file)
        for row in old_model_reader:
            last_model_ids.append(row['Id'])

if path.exists('model.csv'):
    with open('model.csv', 'r') as current_model_file:
        curr_model_reader = csv.DictReader(current_model_file)
        for row in curr_model_reader:
            curr_model_ids.append(row['Id'])

# k=fixId , v=commitId
fix_dict = dict()

if path.exists('fixlist.txt'):
    with open('fixlist.txt', 'r') as fixlist_file:
        line = fixlist_file.readline()
        while line:
            curr_line = line[0:-1] # remove ending \n

            curr_line_split = curr_line.split('\t') # ID\tVERSION\tCOMMIT
            fix_id = str(curr_line_split[0])
            if len(curr_line_split) > 1:
              fix_ver_commit = str(curr_line_split[1])
              if len(curr_line_split) > 2:
                fix_ver_commit += ' (' + curr_line_split[2] + ')'
              else:
                fix_ver_commit += ' (unknown commit)'
            else:
              fix_ver_commit = 'unknown app version (unknown commit)'

            fix_dict[str(fix_id)] = str(fix_ver_commit)
            
            fixed_ids.append(fix_id) 
            line = fixlist_file.readline()

regression_set = set(intersection(curr_model_ids, fixed_ids))



# Detection map: [id] = STATUS
# With STATUS in {'Fixed', 'Open', 'OpenRegression', 'None'}
detection_dict = dict()

stats_risk_dict = dict()

with open(REPORT_FILE_NAME, 'w', encoding='utf-8') as reportFile:

    reportFile.write(report_head)

    with open('model.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:

            if row['Id'] in detection_dict:
              continue

            test_case_result = parse_case_to_test.parse(row)

            reportFile.write(
                buildCaseRowHTML(test_case_result,
                    row['Risk'],
                    row['Vulnerability'],
                    row['Weakness'],
                    row['Threat'],
                    row['Instance'],
                    row['Asset'],
                    row['Countermeasure'],
                    row['Attack'],
                    row['Likelihood Of Exploit'],
                    row['Scan tool'],
                    row['Id'],
                    row['NIST'],
                    regression_set
                )
            )

            if test_case_result == True:
              detection_dict[str(row['Id'])] = 'Fixed'
            else:

              if len(str(row['NIST']))>0:
                nist_fail_set.add(str(row['NIST']))
              
              if row['Id'] in regression_set:
                detection_dict[str(row['Id'])] = 'OpenRegression'
              else:
                detection_dict[str(row['Id'])] = 'Open'

              current_risk = str(row['Risk'].strip().lower())
              if current_risk in stats_risk_dict:
                stats_risk_dict[current_risk] = stats_risk_dict[current_risk] + 1
              else:
                stats_risk_dict[current_risk] = 1

    # TEST FROM DETECTIONS DISAPPEARED FROM LAST MODEL
    if path.exists('last-model.csv'):
      with open('last-model.csv', 'r') as old_model_file:
        old_model_reader = csv.DictReader(old_model_file)
        for row in old_model_reader:

          if row['Id'] in detection_dict:
            continue

          test_case_result = parse_case_to_test.parse(row)

          if test_case_result == True:
            
            with open('fixlist.txt', 'a') as f:
              f.write(row['Id'] + '\t' + app_version.replace('\t', ' ') + '\t' + app_commit_id.replace('\t', ' ') + '\n')

            detection_dict[str(row['Id'])] = 'Fixed'

          elif test_case_result == False:

            print('WARN: Non-fixed vulnerability found (' + row['Id'] + '), putting it back into the model...')
            with open('model.csv', 'a', encoding='utf-8') as f:
                csv_model_writer = csv.writer(f)
                csv_model_writer.writerow( row.values() )
                print('...done')

            if len(str(row['NIST']))>0:
                nist_fail_set.add(str(row['NIST']))

            if row['Id'] in regression_set:
              detection_dict[str(row['Id'])] = 'OpenRegression'
            else:
              detection_dict[str(row['Id'])] = 'Open'

            current_risk = str(row['Risk'].strip().lower())
            if current_risk in stats_risk_dict:
              stats_risk_dict[current_risk] = stats_risk_dict[current_risk] + 1
            else:
              stats_risk_dict[current_risk] = 1

          reportFile.write(
                buildCaseRowHTML(test_case_result,
                    row['Risk'],
                    row['Vulnerability'],
                    row['Weakness'],
                    row['Threat'],
                    row['Instance'],
                    row['Asset'],
                    row['Countermeasure'],
                    row['Attack'],
                    row['Likelihood Of Exploit'],
                    row['Scan tool'],
                    row['Id'],
                    row['NIST'],
                    regression_set
                )
            )

    # ###

    report_footer = """
    </tbody>
    </table>
    </body>
    </html>
    """

    reportFile.write(report_footer)

# Inserts stats table
buildStatsTableHTML(stats_risk_dict, nist_fail_set)

#
####################################################
#

#########################################
### UPDATE DETECTION SPECIFIC HISTORY ###
#########################################

history.updateDetectionsDetail(
  detection_dict, 
  app_version, 
  app_commit_id
)

#
####################################################
#

##############################
### UPDATE GENERAL HISTORY ###
##############################

history.updateGlobalHistory(
  detection_dict, 
  stats_risk_dict, 
  app_version, 
  app_commit_id
)

#
####################################################
#

history.generateHistoryReport()

if path.exists('last-model.csv'):
  os.rename('last-model.csv', '.model-' + datetime.now().strftime("%d%m%Y%H%M").strip() + '.csv')
os.rename('model.csv', 'last-model.csv')