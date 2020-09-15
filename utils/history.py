import os
import csv

from datetime import datetime
from os import path

from utils.html_util import history_report_head_html, history_report_footer_html

def stringifyDictKeys(mDict, separator=';'):
  """
  Description
  """
  dict_str = ''
  for key in mDict:
    dict_str += key + ';'
  return dict_str[0:-1]

def generateHistoryReport(history_path='history', 
  model_name='history'
  ):
  """
  Description
  """

  with open('historyReport.html', 'w', encoding='utf-8') as report_file:
    report_file.write(history_report_head_html)

    with open(history_path + path.sep + model_name + '.csv', 'r') as f:
      model_reader = csv.DictReader(f)
      for row in model_reader:
        curr_html = """
        <div class="timeline-section">
        <div class="timeline-date"> v.""" + str(row['version']) + ' (' + str(row['commit']) + """)</div>
      
        <div class="row">
          <div class="col-sm-4">
            <div class="timeline-box">
              <div class="box-title"></div>
              <div class="box-content">
        """

        curr_risk_split = row['stats_risk'].split(';')
        tot_count = 0
        for curr_risk in curr_risk_split:
          curr_risk_name = curr_risk.split(': ')[0]
          curr_risk_num = curr_risk.split(': ')[1]
          curr_html += '<div class="box-item"><strong>'+curr_risk_name+'</strong>: ' + str(curr_risk_num) + '</div>'
          tot_count = tot_count + int(curr_risk_num)
        
        curr_html += '<div class="box-item"><strong>Total</strong>: '+str(tot_count)+'</div>'
        curr_html += """
                </div>
                <div class="box-footer"></div>
              </div>
            </div>
          </div>
        </div>
        """
        report_file.write(curr_html)

    report_file.write(history_report_footer_html)

def updateDetectionsDetail(
  detection_status_dict,
  app_version,
  app_commit_id,
  history_path='history',
  file_ext='.detection'
):
  """
  """

  history_path = str(history_path)
  file_ext = str(file_ext)

  while history_path.endswith(str(path.sep)) :
    history_path = history_path[0:-1]

  current_date_str = datetime.now().strftime("%d/%m/%Y %H:%M UTC")

  if not path.exists(history_path):
    os.mkdir(history_path, 777)

  history_file_list = os.listdir(history_path)
  for item in history_file_list:

    if (str(item).startswith('.')) or (not str(item).endswith(file_ext)) or (str(item[0:-10]) in detection_status_dict):
      continue

    # Update Detections not found in this version
    original_file = None
    if path.exists(history_path + path.sep + item):
      with open(history_path + path.sep + item,'r') as contents:
          original_file = contents.read()
    with open(history_path + path.sep + item, 'w', encoding='utf-8') as f:
      f.write(current_date_str + '\t' + app_version + '\t' + app_commit_id + '\t' + 'None' + '\n')
      if not(original_file is None):
        f.write(original_file)

  # Update Detections found in this version
  for key in detection_status_dict:
    original_file = None
    if path.exists(history_path + path.sep + key + file_ext):
      with open(history_path + path.sep + key + file_ext,'r') as contents:
        original_file = contents.read()
    with open(history_path + path.sep + key + file_ext, 'w', encoding='utf-8') as f:
      f.write(current_date_str + '\t' + app_version + '\t' + app_commit_id + '\t' + detection_status_dict[key] + '\n')
      if not (original_file is None):
        f.write(original_file)

def updateGlobalHistory(
  detection_status_dict,
  stats_risk_dict,
  app_version,
  app_commit_id,
  history_path='history',
  model_name='history'):
  """
  """

  history_path = str(history_path)
  model_name = str(model_name)

  while history_path.endswith(str(path.sep)) :
    history_path = history_path[0:-1]

  if model_name.endswith('.csv'):
    model_name = model_name[0:-4]

  if not path.exists(history_path + path.sep + model_name + '.csv'):
    with open(history_path + path.sep + model_name + '.csv', 'w', encoding='utf-8') as f:
      head_row = ['version', 
                  'commit', 
                  'detections', 
                  'fixlist', 
                  'stats_number_of_detections', 
                  'stats_risk']
      csv_model_writer = csv.writer(f)
      csv_model_writer.writerow( head_row )

  stats_risk_str = ''
  for key in stats_risk_dict:
    stats_risk_str += key + ': ' + str(stats_risk_dict[key]) + ';'
  stats_risk_str = stats_risk_str[0:-1]

  with open(history_path + path.sep + model_name + '.csv', 'a', encoding='utf-8') as f:
    csv_model_writer = csv.writer(f)

    # Build Detection list, skipping Fixed and None (not found anymore)
    # Build Fix list stringified
    found_detections_dict = dict()
    fixed_ids_str = ''
    for key in detection_status_dict:
      current_detection_status = detection_status_dict[key].strip().lower()
      if not (current_detection_status == 'fixed' or current_detection_status == 'none'):
        found_detections_dict[key] = detection_status_dict[key]
      elif current_detection_status == 'fixed':
        fixed_ids_str += key + ';'

    if len(fixed_ids_str)>0:
      fixed_ids_str = fixed_ids_str[0:-1]

    csv_model_writer.writerow( [app_version, app_commit_id, stringifyDictKeys(found_detections_dict), fixed_ids_str, len(found_detections_dict), stats_risk_str] )