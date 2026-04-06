You are working inside this repository and have access to the full codebase plus BigQuery.

I need you to refactor the current BigQuery product sync implementation based on reviewer feedback.

## Context

Ryan said this PR is causing CodeQL issues and the implementation must be changed to use CLI instead of Python.

Current implementation details in this repo:

* Workflow file: `.github/workflows/deploy-products.yml`
* Current sync script: `scripts/sync_product_bigquery.py`
* Current docs: `docs/BIGQUERY-PRODUCT-SYNC-IMPLEMENTATION.md`
* The workflow currently calls:
  `python scripts/sync_product_bigquery.py --product-file ... --action ... --bq-project ... --bq-dataset ...`

## Important findings from the current implementation

1. The current Python script is not a true upsert.

   * In `scripts/sync_product_bigquery.py`, create/update checks if a product exists, but still inserts a new row.
   * It prints:
     “Product exists - will insert new version (streaming buffer doesn't support DELETE)”
   * This means update creates duplicate rows for the same product name.

2. Documentation currently overstates behavior.

   * Docs say “delete existing row then insert new row”
   * Actual code does not do that for update.

3. Delete support is only partly wired.

   * The Python script has delete logic.
   * But the workflow does not fully handle deleted product files from Git change detection.

4. BigQuery sync is non-blocking in workflow.

   * Deployment succeeds even if sync fails.
   * Preserve this unless there is a very strong repo convention saying otherwise.

## Goal

Replace the Python-based BigQuery sync with a CLI-based implementation in GitHub Actions and/or bash scripts using approved CLI tools only.

Preferred tools:

* `bq`
* `jq`
* `yq`
* bash
* existing GitHub Actions shell logic

Avoid:

* Python
* custom application code for BigQuery sync
* anything likely to trigger CodeQL concerns

## What I want you to do

### Part 1 — Inspect current repo and propose exact changes

Review:

* `.github/workflows/deploy-products.yml`
* any existing changed-files detection logic
* any existing delete handling
* current BigQuery-related env vars and auth setup
* whether `bq`, `jq`, `yq` are already installed or need setup

Then show me a concise implementation plan before editing.

### Part 2 — Implement CLI-based BigQuery sync

Create a bash-based solution, for example:

* `scripts/sync_product_bigquery.sh`

This script should:

* accept:

  * `--product-file`
  * `--action`
  * `--bq-project`
  * `--bq-dataset`
* parse product YAML using `yq`
* determine target table:

  * if `spec.access == "public"` → `external_products`
  * else → `internal_products`
* map fields:

  * name
  * display_name
  * description
  * environments
  * attributes
  * proxies
  * auto_approval
  * sysgen
  * owner_email_address
  * consumer_exposure
  * raw_object

### Part 3 — Fix update semantics properly

For create/update, do NOT append a duplicate row.

Implement one of these approaches, preferring the cleanest CLI-safe option:

1. use a `MERGE` statement via `bq query`
2. or stage a single-row JSON payload and merge into target table by `name`

Requirement:

* one logical current row per product name in each table
* update must replace existing metadata for that product name
* no duplicate rows for the same product caused by update

### Part 4 — Handle delete properly

Implement delete in CLI using `bq query`:

* delete from the correct table where `name = product_name`

Also inspect the workflow and wire deleted file handling end-to-end.
If the current workflow uses changed-files outputs, connect deleted product files so BigQuery delete can actually run when a product file is removed from Git.

If deleted-file handling cannot fully determine metadata from the deleted file path alone, then propose and implement the safest repo-compatible fallback, such as:

* extracting product name from filename if naming convention guarantees it
* or using git diff to retrieve deleted file content from previous revision
* or documenting a temporary limitation if repo constraints make full delete impossible

But do not leave delete half-wired.

### Part 5 — Keep security and sanitization

Current Python logic strips sensitive keys from raw_object based on keywords like:

* secret
* credential
* token
* key
* password

Preserve equivalent sanitization in bash/jq before writing raw_object to BigQuery.

### Part 6 — Update workflow

Modify `.github/workflows/deploy-products.yml` to:

* remove Python-based sync invocation
* call the CLI/bash sync script instead
* install/setup any needed CLI dependencies
* preserve current success/failure behavior where deployment succeeds even if BigQuery sync fails, unless repo conventions clearly require otherwise
* add clear logging around:

  * target table
  * action
  * product name
  * sync success/failure

### Part 7 — Update documentation

Update:

* `docs/BIGQUERY-PRODUCT-SYNC-IMPLEMENTATION.md`
* `scripts/README.md`
* any demo guide references

Make documentation match real behavior exactly.
Do not claim “upsert” unless MERGE or true replacement behavior exists.

## Output format I want from you

1. First, show:

   * files that need to change
   * short explanation of why
   * exact implementation plan

2. Then generate full code changes.

3. For each changed file, clearly show:

   * file path
   * before/after summary
   * final code

4. Highlight any assumptions explicitly as:
   `[Assumption]`

5. If you find a blocker, do not stop early.
   Instead:

   * explain the blocker
   * propose the best repo-compatible fallback
   * implement as much as possible

## Extra instructions

* Reuse existing repo patterns and naming conventions.
* Do not invent fields or schemas that are not already implied by the current implementation.
* Prefer production-safe shell scripting with proper quoting and error handling.
* If BigQuery table schema requires JSON strings instead of native JSON types, preserve compatibility with the current implementation.
* If you need to use temporary SQL files or JSON temp files in workflow, do it cleanly and delete temp files afterward.
* Keep the solution review-friendly and enterprise-safe.

Start by reviewing the current implementation and propose the change plan.
