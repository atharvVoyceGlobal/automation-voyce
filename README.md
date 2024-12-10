#!/bin/bash

cat << 'EOF' > README.md
# Admin/Customer Portal Auto Test

## Test Actions

### 1. Create an Account

- **1.1** Verify the ability to create a new account.
- **1.2** Validate successful creation by checking MongoDB and UI updates.

### 2. Log In Page

- **2.1** Test login functionality with valid and invalid credentials.

### 3. Forgot Password

- **3.1** Ensure the password reset functionality works and verifies securely.

## Admin Portal Pages

### Dashboard

- **2.1** Widgets check with the database.
- **2.2** Compare diagram API data with the database.
- **2.3** Check UI functionality.
- **2.4** Reconcile dashboard widgets data with the Transaction page and Device Usage page.

### Audio vs. Video Report

- **3.1** Compare API data with the database.
- **3.2** Check UI functionality.
- **3.3** Reconcile Databricks data with front-end data.

### Device Usage

- **4.1** Perform data comparison with MongoDB and validate front-end reports.
- **4.2** Reconcile device usage data.

### Language Heatmap Report

- **5.1** Check UI data mapping with the database.

### Language Report

- **6.1** Validate language-specific reports across UI and database.

### Invoices

- **7.1** Compare diagram API data with the database.
- **7.2** Check UI functionality.
- **7.3** Reconcile Databricks data with front-end data.

### Non-Service Calls Report

- **8.1** Verify data integrity with MongoDB and ensure UI accuracy.

### Top Customer Report

- **9.1** Ensure correct ranking of customers based on predefined criteria.

### Video Call Analysis Report

- **10.1** Verify correct metadata from the database and ensure UI accuracy.

### Interpreter HUD Availability Report

- **11.1** Ensure UI functionality and reconcile data with the database.

### Interpreter HUD Routing History

- **12.1** Check interpreter routing history data in UI and MongoDB.

### Activity Monitor

- **13.1** Validate activity logs for accuracy.
- **13.2** Reconcile front-end data with Databricks data.

### Role Hierarchy

- **14.1** Ensure role hierarchy is accurate in UI and database.

### Admin Portal Audit Report

- **15.1** Validate the accuracy of the audit report in UI.
- **15.2** Reconcile data with MongoDB.

### Customer Portal Audit Report

- **16.1** Ensure audit data matches between UI and MongoDB.

### Transactions

- **17.1** Reconcile transaction data between UI, routing history, and MongoDB.

### Interpreter HUD Dashboard

- **18.1** Widgets check with the database.
- **18.2** Reconcile data with the Transaction page and Routing History.

### QA HUD

- **19.1** Compare diagram data with the database.
- **19.2** Check UI functionality.
- **19.3** Reconcile Databricks data with front-end data.

### QA Report

- **20.1** Same steps as QA HUD, focusing on the correctness of QA report data.

## Requirements

To run the tests, install the following dependencies listed in `requirements.txt`:

```plaintext
alembic==1.13.1
allure-pytest==2.13.3
allure-python-commons==2.13.3
Appium-Python-Client==3.1.1
assertpy==1.1
attrs==23.1.0
browsermob-proxy==0.8.0
certifi==2023.11.17
cffi==1.16.0
charset-normalizer==3.2.0
click==8.1.7
contourpy==1.2.0
cryptography==42.0.5
cycler==0.12.1
databricks-cli==0.17.7
databricks-connect==13.2.1
databricks-sdk==0.6.0
databricks-sql-connector==3.1.0
dnspython==2.4.2
et-xmlfile==1.1.0
exceptiongroup==1.1.2
execnet==2.0.2
fonttools==4.48.1
googleapis-common-protos==1.60.0
greenlet==2.0.2
grpcio==1.57.0
grpcio-status==1.57.0
h11==0.14.0
idna==3.4
iniconfig==2.0.0
kiwisolver==1.4.5
logging==0.4.9.6
lz4==4.3.2
Mako==1.2.4
MarkupSafe==2.1.3
matplotlib==3.8.2
MouseInfo==0.1.3
numpy==1.26.4
oauthlib==3.2.2
openpyxl==3.1.2
outcome==1.2.0
packaging==23.1
pandas==2.1.4
pillow==10.2.0
pluggy==1.5.0
protobuf==4.24.1
psycopg2-binary==2.9.9
py4j==0.10.9.7
pyarrow==14.0.2
PyAutoGUI==0.9.54
pycparser==2.21
PyGetWindow==0.0.9
PyJWT==2.8.0
pymongo==4.6.2
PyMsgBox==1.0.9
pyobjc-core==10.1
pyobjc-framework-Cocoa==10.1
pyobjc-framework-Quartz==10.1
pyodbc==4.0.39
pyOpenSSL==24.0.0
pyparsing==3.1.1
pyperclip==1.8.2
PyRect==0.2.0
PyScreeze==0.1.30
PySocks==1.7.1
pyspark==3.4.1
pytest==8.2.0
pytest-order==1.2.0
pytest-sqlalchemy==0.2.1
pytest-xdist==3.5.0
python-dateutil==2.8.2
pytweening==1.0.7
pytz==2023.3
requests==2.31.0
rubicon-objc==0.4.7
selenium==4.20.0
six==1.16.0
sniffio==1.3.0
sortedcontainers==2.4.0
SQLAlchemy==2.0.30
SQLAlchemy-Utils==0.41.2
tabulate==0.9.0
thrift==0.16.0
trio==0.22.2
trio-websocket==0.10.3
typing_extensions==4.9.0
tzdata==2023.3
urllib3==1.26.16
urllib3-secure-extra==0.1.0
wsproto==1.2.0
yolk3k==0.9


###Installation


Clone this repository
Install the required dependencies using pip:

pip install -r requirements.txt


#####Running Tests
You can execute tests and generate Allure reports by running the following commands:

Run the tests and generate Allure report data:
python -m pytest --alluredir=test_results/


Serve the Allure report:
allure serve test_results/

