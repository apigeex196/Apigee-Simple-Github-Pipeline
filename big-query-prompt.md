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
========================================================

You are a senior Python data engineer.

Create a production-style Python script named `inspect_bigquery_apigee.py` that connects to Google BigQuery using service account credentials from the environment and helps analyze an existing Apigee-to-BigQuery setup.

Context:
- BigQuery authentication is already working in my environment.
- Project ID: `gcp-prj-apigee-dev-np-01`
- Existing datasets found:
  - `api_products`
  - `dev_apps`
  - `developers`
- Existing tables found:
  - `api_products.external_products`
  - `api_products.internal_products`
  - `dev_apps.external_devapps`
  - `dev_apps.internal_devapps`
  - `developers.external_devs`
  - `developers.internal_devs`

Goal:
I want a Python script that inspects these datasets and tables and helps answer:
1. Can we reuse these existing datasets/tables?
2. Are they likely part of the existing ingestion pipeline?
3. What schema do they have?
4. Do they contain potentially sensitive fields such as:
   - consumerKey
   - consumerSecret
   - apiKey
   - secret
   - token
   - password
   - credential
5. Should we create new tables only for derived/custom application data?

Requirements:
1. Use Python.
2. Use the official `google-cloud-bigquery` package.
3. Read credentials using normal Google auth resolution:
   - `GOOGLE_APPLICATION_CREDENTIALS`
   - or default application credentials
4. Keep the script runnable from terminal:
   - `python inspect_bigquery_apigee.py`
5. Use clear functions with good naming and comments.
6. Add error handling for:
   - authentication failure
   - project access errors
   - dataset/table not found
   - query errors
7. Print clean console output with sections.

Script behavior:
1. Connect to BigQuery for project `gcp-prj-apigee-dev-np-01`
2. Verify access by running:
   - `SELECT 1 AS ok`
3. For each dataset:
   - check existence
   - list tables
4. For each table:
   - print full schema:
     - column name
     - type
     - mode
   - detect suspicious/sensitive column names using case-insensitive matching against:
     - consumerkey
     - consumersecret
     - apikey
     - secret
     - token
     - password
     - credential
   - fetch row count using a safe query
   - fetch 3 sample rows
   - print sample rows in a readable but truncated format
5. Generate a final recommendation section:
   - If tables already exist and names match apps/products/developers, print that these are likely reusable core pipeline tables.
   - If suspicious columns are found, warn that data should be sanitized and those fields should not be newly inserted into BigQuery.
   - Recommend using existing datasets for existing pipeline entities.
   - Recommend creating separate new tables only for:
     - derived analytics
     - migration tracking
     - custom application-specific processed outputs
6. Output a structured summary like:
   - Connection status
   - Datasets status
   - Tables inspected
   - Sensitive columns found
   - Reuse vs create recommendation

Implementation details:
- Use `bigquery.Client(project=PROJECT_ID)`
- Use dataset and table metadata APIs where possible
- Use SQL only where helpful for counts/sample rows
- Truncate long field values in sample rows to avoid dumping huge JSON
- Make the code modular with functions like:
  - `get_client()`
  - `test_connection()`
  - `list_dataset_tables()`
  - `get_table_schema()`
  - `find_sensitive_columns()`
  - `get_row_count()`
  - `get_sample_rows()`
  - `print_final_recommendation()`
- Include a `main()` function and `if __name__ == "__main__":`

Also generate:
1. a `requirements.txt` file containing needed dependencies
2. a short README section at the top of the script as a docstring explaining:
   - how to install dependencies
   - how to set `GOOGLE_APPLICATION_CREDENTIALS`
   - how to run the script

Make the code real, complete, and runnable. Do not leave placeholders like "implement later".

