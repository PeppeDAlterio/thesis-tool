#!/bin/sh

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] ; then
    echo "Usage: run.sh app_name app_version commit_id image_name image_tag app_uri [tool1 tool2 ... toolN]"
    exit -1
fi

python3 sys_scan.py "$@"
python3 test_and_report.py "$1" "$2" "$3"