# Semi-automated security testing tool

## Software requirements
System:

    python3-dev python3 python3-pip python3-setuptools curl gcc libpq-dev python3-dev python3-wheel
    
Python:

    libxml2-python3 requests-html wheel requests==2.20.1

## Usage
### Test and report

    sh run.sh <APP_NAME> <APP_VERSION> <COMMIT_ID> <IMAGE_NAME> <IMAGE_TAG> <APP_URI> [tool1 tool2 ... toolN]

- APP_NAME, application name
- APP_VERSION, application version
- COMMIT_ID, commit id
- IMAGE_NAME, Docker image name
- IMAGE_TAG, Docker image tag
- APP_URI, application URI (e.g. web application url)
- tool, list of scanning tools to use in [anchore, zap, joomscan]

#### Output
- report.html, main report with detection and proposed countermeasures
- historyReport.html, historical timeline report

### Detection timeline

    python timeline.py <DETECTION_ID>

- DETECTION_ID, id of the detection as shown in the report 
