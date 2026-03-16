
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

===================================================================================

Act as a senior Python architect working inside this repo. Continue from the current refactor state. Do not restart from scratch. Finish the missing part of the three-layer architecture.

CURRENT STATUS
The repo already has:
- models for InventoryProxyRecord / VerifiedProxyRecord / MigrationProxyRecord
- OPDK verification client
- verify command
- docs describing the separation
- warnings around inventory-based extraction

But the critical gap remains:
- extract from verified data is NOT fully implemented
- discover.py currently says something like:
  "Extract from verified data not yet fully implemented"
- YAML generation still depends on old ESP/inventory-style flow
- the real architectural fix is incomplete until verified OPDK data can actually drive extraction

GOAL
Finish the missing implementation so migration extraction and proxy.yaml generation can run from VerifiedProxyRecord / authoritative OPDK verification results, not only from heuristic inventory rows.

NON-NEGOTIABLE REQUIREMENTS
1. Do NOT remove the existing inventory flow.
2. Do NOT break the existing extract flow for legacy/demo use.
3. Add a proper verified extraction path that is authoritative-first.
4. Keep warnings when users attempt extraction from non-authoritative inventory-only data.
5. Reuse existing code where safe; refactor carefully rather than duplicating logic.

WHAT TO IMPLEMENT

1) COMPLETE VERIFIED EXTRACTION PATH
Implement the missing logic in discover.py (or the appropriate extraction orchestration module) so that:
- `extract --use-verified <path-to-verified-summary.json>` works end-to-end
- it loads VerifiedProxyRecord
- it converts verified data into the structure expected by migration generation
- it generates migration artifacts from verified data
- it does NOT stop with a placeholder or not-implemented message

If the CLI currently expects a directory or file, standardize it clearly and document it.

2) UPDATE YAML GENERATION TO SUPPORT VERIFIED INPUTS
Inspect the existing YAMLGenerator / yaml generation module and modify it so it can accept:
- VerifiedProxyRecord directly, or
- a normalized migration model derived from VerifiedProxyRecord

Do NOT fake ESP fields that do not exist.
Do NOT silently pretend verified data contains everything inventory data had.
Where data is missing:
- generate warnings
- include evidence/confidence metadata
- continue best-effort where safe

Expected verified-derived fields to map when available:
- proxyName
- revisions
- deployedRevision
- basePath
- virtualHosts
- environment
- target/backend URLs
- sourceType = "opdk-management"
- authoritative = true

3) CREATE A CLEAR TRANSFORMATION STEP
Add a dedicated transformation layer/function such as:
- verified_to_migration(...)
or similar

Purpose:
- convert VerifiedProxyRecord -> MigrationProxyRecord
- centralize field mapping
- centralize warnings for missing fields
- avoid spreading mapping logic across discover.py and YAMLGenerator

MigrationProxyRecord should explicitly carry:
- proxyName
- basePath
- targetUrls / backends
- environment
- revisions / deployedRevision
- authoritative
- sourceType
- evidenceLevel / confidence
- warnings list

4) AUTHORITATIVE OUTPUT LABELING
Any migration artifact generated from verified data must clearly include metadata showing:
- sourceType: opdk-management
- authoritative: true
- confidence/evidence notes
- warnings for any missing fields

Any migration artifact generated from inventory-only data must clearly include metadata showing:
- sourceType: inventory-heuristic
- authoritative: false
- warning that this output is not source-of-truth

5) KEEP LEGACY FLOW, BUT MAKE IT HONEST
If legacy extract from ESP/inventory still exists:
- keep it working
- label it clearly as heuristic / non-authoritative
- do not let it masquerade as authoritative migration truth

6) FILE OUTPUTS
For verified extraction, generate outputs under a sensible structure, for example:
output/extract/<proxyName>/<timestamp>/
or reuse the current extract output structure if one already exists.

Ensure output includes:
- proxy.yaml
- migration-summary.json (or similar)
- warnings file if appropriate

If verified-summary.json is the input, preserve traceability back to it.

7) DOCS
Update the existing docs to reflect the finished implementation:
- how to run verify
- how to run extract from verified data
- how verified extraction differs from inventory extraction
- what output files get created
- which fields are authoritative vs best-effort
- what limitations remain

Update or add a demo doc with copy-paste commands for:
- verify demo
- extract from verified demo
- extract from inventory demo
- showing the warning difference between authoritative and heuristic outputs

8) TESTS
Add or update tests for:
A. VerifiedProxyRecord -> MigrationProxyRecord transformation
B. YAML generation from verified input
C. extract --use-verified no longer stops with a placeholder
D. output metadata marks authoritative=true for verified flow
E. legacy inventory flow remains authoritative=false
F. missing verified fields produce warnings, not fake values

IMPLEMENTATION GUIDELINES
- Inspect current YAMLGenerator instead of replacing it blindly
- Reuse existing output structures where practical
- Do not invent OPDK response fields that are not present
- Prefer explicit transformation functions over ad hoc dict passing
- Keep changes minimal but complete
- Remove any placeholder message that says verified extraction is not yet implemented
- Make the finished path actually runnable

IMPORTANT
Do not stop at “partial support.”
Do not leave the repo in a state where docs claim verified extraction exists but the code still cannot generate proxy.yaml from verified input.

DELIVERABLES
After changes, provide:
1. changed files list
2. brief explanation of each change
3. exact command to run verify
4. exact command to run extract using verified-summary.json
5. example expected output files
6. honest remaining limitations

FIRST STEP
Inspect:
- current discover.py extract flow
- current YAMLGenerator interface
- any existing not-implemented / placeholder branch for verified extraction
- current output structure for extract

Then finish the implementation directly in this repo.
Do not respond with “architecture is ready” unless `extract --use-verified ...` actually generates migration artifacts successfully.
