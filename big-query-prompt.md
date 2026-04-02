You are a senior Python/GitHub Actions engineer working inside my existing repository.

Your job is to inspect this project and implement BigQuery sync for API PRODUCT metadata only.

IMPORTANT BUSINESS CONTEXT
- This repository supports GitOps flow for API Products.
- Jira requirement:
  - API Producers define API Product config in Git
  - pipeline triggers on product config changes
  - pipeline performs Create / Update / Delete on API Products
  - product is deployed to Apigee X and OPDK
  - after successful deployment, product metadata is updated in BigQuery
- BigQuery sync is ONLY for API PRODUCT metadata
- This task is NOT about proxy discovery
- Do NOT add proxy extraction or proxy BigQuery tables
- Do NOT sync developer apps or developers in this task

BIGQUERY TARGET
Project ID:
- gcp-prj-apigee-dev-np-01

Dataset:
- api_products

Target table:
- choose the correct table already used by this repo flow, likely one of:
  - external_products
  - internal_products

If selection between external_products and internal_products is based on product access/exposure, inspect the project and implement the correct mapping.

BIGQUERY TABLE SCHEMA
The target product table has these 11 columns:

1. name STRING REQUIRED
2. display_name STRING NULLABLE
3. description STRING NULLABLE
4. environments STRING REPEATED
5. attributes JSON NULLABLE
6. proxies STRING REPEATED
7. auto_approval BOOLEAN NULLABLE
8. sysgen STRING NULLABLE
9. owner_email_address STRING NULLABLE
10. consumer_exposure STRING NULLABLE
11. raw_object JSON NULLABLE

WHAT TO INSERT
Map product GitOps config / deployed product state into these columns:

- name -> metadata.name
- display_name -> spec.displayName if present else metadata.name
- description -> metadata.description
- environments -> spec.environments
- attributes -> spec.attributes as JSON
- proxies -> spec.proxies as repeated string array
- auto_approval -> boolean derived from spec.approval == "auto"
- sysgen -> metadata.sysgen
- owner_email_address -> map from config if present, otherwise null unless there is an existing reliable source in repo
- consumer_exposure -> derive from the repo’s product access/exposure field, likely from spec.access or equivalent
- raw_object -> full sanitized product object as JSON

STRICT RULES
- Do NOT insert secrets or credentials
- Do NOT insert consumer keys
- Do NOT insert consumer secrets
- Do NOT touch proxy discovery code for this task
- Do NOT create a new BigQuery schema if the existing table already matches
- Reuse the existing api_products table structure
- Keep the current deployment behavior intact
- BigQuery update must happen only AFTER successful deployment to required targets
- BigQuery should reflect accurate final deployed state

DELETE BEHAVIOR
- Jira requires Create / Update / Delete
- Inspect current repo and determine whether delete flow exists
- If delete flow exists, implement matching BigQuery delete
- If delete flow does not yet exist, clearly identify the gap and implement the BigQuery side in the safest way possible based on current structure
- Prefer real delete from BigQuery if there is no status column in schema

YOUR TASKS
1. Inspect the repository and identify:
   - the GitHub workflow for product deployment
   - the composite action / script used for product deployment
   - the product schema/config file
   - where product YAML is parsed
   - where create/update/delete decisions are made
   - the best integration point for BigQuery sync

2. Summarize the files and functions you found before writing code.

3. Implement BigQuery sync with minimal safe changes.

4. Add code to:
   - build a BigQuery row from the product config / deployed product payload
   - choose the right target table (external_products or internal_products)
   - insert row on create
   - update row on update
   - delete row on delete if product is deleted

5. Use the official Python BigQuery client if Python is already used in this flow.
   If this workflow is shell-based and another language is more natural in the repo, inspect first and choose the best fit. But prefer the smallest safe change.

6. Add proper logging for:
   - product name
   - operation type
   - selected BigQuery dataset/table
   - BigQuery success/failure
   - rows inserted/updated/deleted

7. Make configuration environment-driven where appropriate:
   - BQ_PROJECT_ID default gcp-prj-apigee-dev-np-01
   - BQ_DATASET default api_products

8. Keep code production-ready and repo-aligned.
   Do not invent non-existing fields unless clearly marked optional/null.

EXPECTED OUTPUT
Please generate:
1. the exact files to modify
2. the code changes
3. any new helper module/script needed
4. any requirements/dependency updates
5. a short explanation of how the flow works now

IMPLEMENTATION GUIDANCE
- First inspect existing files such as:
  - .github/workflows/deploy-products.yml
  - .github/actions/deploy-product/action.yml
  - apiproduct.schema.json
  - any product scripts/helpers
- Reuse existing parsed product payload rather than reparsing from scratch if possible
- If a full deployed Apigee response object is available after deployment, prefer using that for raw_object
- If not available, use the sanitized Git product object as raw_object
- For repeated BigQuery fields, ensure arrays are passed correctly
- For JSON fields, pass valid JSON/dict objects in the format expected by the BigQuery client

VERY IMPORTANT
Before coding:
- tell me exactly which files you inspected
- show where the BigQuery integration point should be
- explain how you will map each of the 11 BigQuery columns
Then generate the code.
Do not give placeholders. Generate real repo-fitting code.



=============================

Follow-up prompt after Copilot inspects the repo

Use this right after the first prompt:


Now implement the change with the smallest safe diff.

Rules:
- do not rewrite the product deployment flow
- extend it only
- keep existing behavior intact
- BigQuery sync must run only after successful deployment
- use the existing product object already available in the workflow/action
- for update, merge by product name
- for delete, remove the row from BigQuery if the product is deleted and no status column exists
- choose external_products vs internal_products using the repo’s existing access/exposure logic
- if owner_email_address is not reliably available, write null and document it clearly
- raw_object must be the full sanitized product object JSON

Show me:
1. exact files changed
2. exact code added
3. how create/update/delete are handled
4. how each BigQuery column is populated



======================================
Create a helper script/module for BigQuery product sync that fits this repo.

It must provide functions like:
- build_bigquery_product_row(product_config: dict) -> dict
- determine_product_table(product_config: dict) -> str
- upsert_product_metadata(row: dict, table_name: str) -> None
- delete_product_metadata(product_name: str, table_name: str) -> None



Hi Team,

I’ve raised a PR for BigQuery product sync implementation:
PR: Feat/bigquery product sync (#202)

This adds metadata sync to BigQuery after successful product deployment.

Could you please review and approve when you get a chance?

Thanks!

Requirements:
- project: gcp-prj-apigee-dev-np-01
- dataset: api_products
- tables: external_products / internal_products
- schema:
  name, display_name, description, environments, attributes, proxies, auto_approval, sysgen, owner_email_address, consumer_exposure, raw_object

Use real code, error handling, logging, and repo-appropriate style.
