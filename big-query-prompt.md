Help me set up and test Google BigQuery access in Python using a service account JSON key.

Context:
- I already have the BigQuery service account JSON key file locally
- I want to create a Python script named test_bigquery.py
- I want to use environment variables, not hardcoded secrets
- The environment variables are:
  - GOOGLE_APPLICATION_CREDENTIALS = full path to the JSON key file
  - BQ_PROJECT_ID = Google Cloud project id
- I want to run this from VS Code terminal on Windows PowerShell

Tasks:
1. Generate a complete Python file named test_bigquery.py
2. Use package: google-cloud-bigquery
3. Do NOT hardcode any secrets
4. Read:
   - GOOGLE_APPLICATION_CREDENTIALS from environment
   - BQ_PROJECT_ID from environment
5. The script must:
   - print whether GOOGLE_APPLICATION_CREDENTIALS is set
   - print whether BQ_PROJECT_ID is set
   - verify whether the credentials file exists
   - connect to BigQuery
   - list all datasets in the project
   - for each dataset, list all tables
   - run a test query: SELECT 1 AS ok
   - print clean readable output
   - handle errors cleanly
   - distinguish as much as possible between:
     - missing env vars
     - missing file path
     - invalid credentials
     - permission denied
     - project not found
     - dataset/table errors
   - never print private key contents
6. Add a main() function and make the script runnable from terminal
7. Also show the exact pip install command
8. Also show the exact Windows PowerShell commands to set:
   - GOOGLE_APPLICATION_CREDENTIALS
   - BQ_PROJECT_ID
9. Also show how to verify the variables in PowerShell using echo
10. Keep the code clean, production-style, and fully copy-paste ready

Important:
- Assume Windows path example like:
  C:\keys\sa-bigquery.json
- Assume project id example like:
  gcp-prj-apigee-dev-np-01
- Output full code, not partial snippets
- After the code, also provide:
  - pip install command
  - PowerShell commands to set env vars
  - command to run the script

Expected example commands to include:
- pip install google-cloud-bigquery
- $env:GOOGLE_APPLICATION_CREDENTIALS="C:\keys\sa-bigquery.json"
- $env:BQ_PROJECT_ID="gcp-prj-apigee-dev-np-01"
- echo $env:GOOGLE_APPLICATION_CREDENTIALS
- echo $env:BQ_PROJECT_ID
- python test_bigquery.py



========================================================

Hi Shimmy,

It looks like the email containing the service account key is restricted (IRM enabled), and I’m unable to copy or extract the JSON content. 

Could you please share the service account key as:
- a .json file attachment, OR
- a secure download link (Drive / OneDrive / etc.)

Currently, the permissions prevent copying, so I can’t use the key for integration.

