
Act as a senior Python architect working inside this repo. Do not give high-level advice only. Make the changes directly in code, preserve existing working behavior, and explain each changed file briefly.

GOAL
Fix the architectural flaw in the proxy-discovery tool: it currently mixes inventory/discovery metadata (Excel/ESP) with authoritative migration truth. We need to separate these responsibilities clearly so inventory reporting remains useful, but migration extraction and verification use authoritative sources.

WHAT IS WRONG TODAY
- The tool treats ESP / Excel-style metadata as if it were source-of-truth for migration.
- Inventory classification and migration extraction are mixed together.
- ESP enrichment and heuristic fields like mtlsEvidenceLevel are okay for reporting, but should NOT be treated as authoritative migration truth.
- The architecture needs a clean separation between:
  1) Inventory layer
  2) Verification layer
  3) Migration extraction layer

WHAT TO IMPLEMENT
Refactor the proxy-discovery tool into three clearly separated layers without breaking existing CLI behavior more than necessary.

1. INVENTORY LAYER
Purpose:
- Fast discovery, filtering, reporting, triage

Allowed sources:
- Excel
- ESP
- cached exports

Responsibilities:
- filter proxies by frontend auth / backend auth
- generate CSV / JSON inventory reports
- compute heuristic fields like mtlsEvidenceLevel
- clearly mark output as inventory / heuristic / non-authoritative

Important:
- Keep current inventory functionality working
- Rename or label outputs/docs so they are clearly “inventory” or “heuristic”, not source-of-truth

2. VERIFICATION LAYER
Purpose:
- Confirm authoritative proxy metadata from management APIs

Authoritative source for now:
- OPDK Management API on port 8080 using Basic Auth

Use env vars:
- OPDK_BASE_URL
- OPDK_ORG
- OPDK_ENV
- OPDK_PROXY_NAME
- OPDK_USER
- OPDK_PASS

Responsibilities:
- fetch authoritative metadata for a proxy using:
  GET /v1/organizations/{org}/apis/{proxyName}
  GET /v1/organizations/{org}/environments/{env}/apis/{proxyName}
- return normalized verified fields such as:
  - proxyName
  - revisions
  - deployedRevision
  - basePath
  - virtualHosts
  - environment
  - targets/backend URLs (best effort)
  - source = "opdk-management"
  - authoritative = true

Important:
- This layer must NOT depend on Excel or ESP
- Use Basic Auth only
- Handle 401/403/404/non-JSON cleanly

3. MIGRATION EXTRACTION LAYER
Purpose:
- Generate migration-ready artifacts ONLY from verified / authoritative inputs
- Do not rely on Excel/ESP heuristics for final migration truth

Responsibilities:
- consume normalized verified data from the verification layer
- generate migration files such as proxy.yaml only when authoritative verification exists
- where required fields are missing, generate warnings instead of pretending completeness
- mark outputs with a confidence / evidence section

IMPORTANT ARCHITECTURAL RULES
- Inventory != Verified truth
- Verified truth != full migration truth unless explicitly confirmed
- Heuristic data must be labeled clearly as heuristic
- OPDK management responses are the source of truth for phase-2 verification
- Do not silently combine heuristic and authoritative data into one undifferentiated model

REFACTOR REQUIREMENTS
1. Introduce clear models or dataclasses / typed structures for:
   - InventoryProxyRecord
   - VerifiedProxyRecord
   - MigrationProxyRecord
2. Ensure these models are not casually interchangeable
3. Add a field such as:
   - evidenceLevel
   - authoritative
   - sourceType
   so the tool always knows what kind of data it is handling
4. Extract ESP-specific code behind a clearly named inventory adapter/client
5. Extract OPDK-specific code behind a verification adapter/client
6. Stop using ESP enrichment to imply migration completeness
7. Make proxy.yaml generation depend on verified inputs, not raw Excel/ESP rows
8. Keep backward compatibility where reasonable, but prefer correctness over hidden magic

CLI CHANGES
Keep existing inventory command, but make its purpose explicit.

Expected CLI structure:
- inventory
  - uses Excel/ESP sources
  - outputs reports only
  - labels output as non-authoritative / heuristic where applicable

- verify
  - new or improved command
  - uses OPDK Management API only
  - saves raw authoritative responses
  - prints clean summary
  - outputs normalized verified record

- extract
  - should no longer assume Excel/ESP inventory is enough for migration truth
  - should either:
    a) require verified input, or
    b) run verification first before generating migration artifacts

If the current extract command is too coupled, refactor it carefully rather than patching around the problem.

OUTPUTS
For verification, save raw responses like:
output/opdk_probe/<proxyName>/<timestamp>/apis.json
output/opdk_probe/<proxyName>/<timestamp>/env_apis.json

Also save a normalized verified summary file, for example:
output/opdk_probe/<proxyName>/<timestamp>/verified-summary.json

For inventory outputs, keep current CSV/JSON outputs but label them as inventory / heuristic.

DOCS TO UPDATE
Update README / HOW-IT-WORKS / relevant docs to clearly state:
- Inventory uses Excel/ESP/cached exports and is heuristic
- Phase-2 verification uses OPDK Management API (port 8080, Basic Auth) as source of truth
- Migration extraction should use verified data, not inventory-only data

Also add or update demo-oriented documentation that explains:
- what changed architecturally
- what each command does now (`inventory`, `verify`, `extract`)
- which outputs are heuristic vs authoritative
- how to run a quick local demo
- how to run a verification demo against one known proxy
- what expected console output and output files should look like
- what limitations still remain

TESTS TO ADD OR UPDATE
Add/adjust tests for:
1. inventory records remain non-authoritative
2. verified records come only from OPDK verification client
3. migration generation refuses or warns when only inventory data is available
4. 401/403/404/non-JSON errors in verification layer
5. normalization of OPDK verification responses
6. clear separation between inventory models and verified models

IMPLEMENTATION STYLE
- Make minimal but correct structural changes
- Prefer small focused modules over giant files
- Reuse existing code where safe
- Remove misleading naming where possible
- Add comments only where they add real value
- Do not leave TODO placeholders
- Do not hallucinate API fields; inspect current code and existing OPDK probe script first
- If there is already an opdk_probe.py or similar, integrate it properly instead of duplicating logic

IMPORTANT DELIVERY REQUIREMENT
Do not stop after code changes. Also document exactly what you changed and how to demo it.

Create or update documentation files so another developer can:
1. understand the new architecture quickly
2. run the inventory flow
3. run the verify flow
4. run the extract flow
5. see which files are generated
6. understand which outputs are authoritative and which are heuristic

Add a concise demo guide with copy-paste commands for:
- inventory demo
- verify demo
- extract demo
- optional sanity test

DELIVERABLES
After making changes, provide:
1. list of changed files
2. short explanation of each file change
3. whether inventory, verify, and extract flows now have clear separation
4. exact commands to demo the new behavior
5. where the documentation was added or updated
6. any remaining limitations honestly

FIRST STEP
Before changing code, inspect the current repo and identify:
- where inventory logic lives
- where ESP-specific logic lives
- where YAML generation lives
- whether an OPDK probe/verification script already exists

Then implement the refactor directly in this repo.

Do not just modify code silently. Update the repo docs so a reviewer can validate the refactor and run the demo without reading the source code.
