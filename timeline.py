# ######################### #
# ARGV:                     #
# [0] timeline.py           #
# [1] Detection ID          #
# ######################### #

import sys

from os import path

from utils.html_util import timeline_head_html as head_html
from utils.html_util import timeline_foot_html as foot_html

if len(sys.argv) < 2:
    print('Usage: timeline.py detectionId')
    exit(0)

detection_id = str(sys.argv[1]).strip()

if not path.exists('history/' + detection_id + '.detection'):
    raise ValueError('Detection ID not found')

head_html = head_html.replace('$detectionId$', detection_id)

with open('history/' + detection_id + '.detection', 'r', encoding='utf-8') as detection_timeline_f:
    with open(detection_id + '.html', 'w', encoding='utf-8') as detection_timeline_html_f:
        detection_timeline_html_f.write(head_html)

        write_right = True

        line = detection_timeline_f.readline()
        while line:

            # DATE\tAPP_VERSION\tCOMMIT\tSTATUS
            # With Status in {Fixed, Open, OpenRegression, None}
            curr_line_split = line.split('\t')

            date = curr_line_split[0].strip()
            app_version = curr_line_split[1].strip()
            commit_id = curr_line_split[2].strip()
            status = curr_line_split[3].strip().lower()

            curr_html = ''

            if write_right:
                curr_html = """
                <div class="container right">
                    <div class="content">
                    <h2>""" + date + """
                    </h2>
                    <p>
                """
            else:
                curr_html = """
                <div class="container left">
                    <div class="content">
                    <h2>""" + date + """
                    </h2>
                    <p>
                """

            curr_html += """
            Application version: v. """ + app_version + """
            <br>
            Commit id: """ + commit_id + """
            <br>
            """

            if status == 'none':
                curr_html += """
                <b style='color: blue;'>NOT FOUND</b>
                """
            elif status == 'open':
                curr_html += """
                <b style='color: orange;'>FOUND</b>
                """
            elif status == 'fixed':
                curr_html += """
                <b style='color: green;'>FIXED</b>
                """
            elif status == 'openregression':
                curr_html += """
                <b style='color: red;'>FOUND AGAIN</b>
                """
                
            curr_html += """
                </p>
                </div>
            </div>
            """
                
            detection_timeline_html_f.write(curr_html)

            write_right = not write_right

            line = detection_timeline_f.readline()

        detection_timeline_html_f.write(foot_html)

