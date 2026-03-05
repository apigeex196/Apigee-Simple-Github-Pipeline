You have access to this repo + local intranet. Implement Andre’s “Filtered Inventory” proposal end-to-end with SAFE DEFAULTS (no need to ask Andre).

Repo paths (real):
- Main script: enterprise-apigeex-applications/proxy-discovery/demo-discovery-tool.py
- Schemas: 
  - enterprise-apigeex-applications/proxy-discovery/apiproxy.schema.json
  - enterprise-apigeex-applications/apiproxy.schema.json
Inputs available:
- Excel inventory: apigee-proxies-export-2026-02-23-154847.xlsx (sheet: Proxies) contains Org, Env, Name, Base Path, Esp ValidAuthTypes, Esp EndpointAuthType, Esp X509CertAlias

Core concept (Andre):
- Frontend/proxy auth models are in ESP as: validAuthTypes (Excel column: "Esp ValidAuthTypes")
- Backend/target auth models are in ESP as: validAuthTypesExt (not in Excel; must be fetched from ESP JSON when needed)
- Backend may also have a single value field "endpointAuthType" (Excel column: "Esp EndpointAuthType")

SAFE DEFAULT DECISIONS (do not ask anyone):
- Matching is EXACT token match by default (case-insensitive), not substring.
- No implicit aliasing between oauth and LIAMOAuth; treat tokens as distinct.
- If both frontend and backend filters are provided, require BOTH to match (scope AND).
- Provide optional flags to enable aliasing and partial match, but default them OFF.

What to implement:

1) Add an `inventory` command to demo-discovery-tool.py that produces a filtered proxy inventory report.
   CLI:
   - inventory --env <env> --out <dir>
   - --source excel|esp (default excel)
   - --excel <path> (default points to the uploaded xlsx path above)
   - --filter-frontend-auth "<comma-separated tokens>"   (filters frontend list)
   - --filter-backend-auth "<comma-separated tokens>"    (filters backend list)
   - --filter-op OR|AND (default OR)   # within each filter list
   - --scope frontend|backend|both (default both)
   - --export csv (optional)
   - --generate-yaml (optional; if set, generate YAML for matched proxies using existing generator flow)
   Optional (default OFF):
   - --match partial (else exact)
   - --enable-aliases true/false (default false)

2) Data normalization:
   - Parse frontend auth models from Excel column "Esp ValidAuthTypes":
     - split by comma
     - trim spaces
     - lowercase for comparison
     - store original tokens for output
   - Parse backend single auth from "Esp EndpointAuthType" similarly.
   - Parse X509 alias presence from "Esp X509CertAlias" (non-empty string means alias present).

3) Filtering logic:
   - Let F = frontend filter tokens (if provided)
   - Let B = backend filter tokens (if provided)
   - Frontend candidates are evaluated against:
     - frontendModels = tokens from Esp ValidAuthTypes
   - Backend candidates are evaluated against:
     - backendModels = tokens from ESP validAuthTypesExt if available, else fallback to [endpointAuthType] from Excel
   - If --scope=both:
     - If both filters provided: require (frontend matches) AND (backend matches)
     - If only one filter provided: require the provided filter matches its scope
   - OR vs AND applies inside each scope list:
     - OR: any token present
     - AND: all tokens present
   - Exact matching by default. If --match partial, allow substring match.

4) ESP enrichment only when needed:
   - When user provides --filter-backend-auth OR when --scope includes backend and --source=esp:
     - call the existing ESP discovery function already used by the tool to fetch per-proxy JSON
     - extract `validAuthTypesExt` if present
     - use it as backendModels (replaces Excel endpointAuthType fallback)
   - Cache results locally under output/<env>/.cache to avoid repeated calls.

5) Output:
   - Always write JSON report: <out>/<env>/filtered-inventory.json
     Each record:
       proxyName, org, env, basePath,
       frontendModels (original), backendModels (original),
       endpointAuthType, x509CertAlias,
       matchedBy: "frontend"|"backend"|"both",
       mtlsEvidenceLevel:
         - "high" if x509CertAlias non-empty
         - "medium" if backendModels contains "clientcert" token
         - "low" if frontendModels contains "clientcert" token
   - If --export csv, write: <out>/<env>/filtered-inventory.csv with columns:
       proxyName, org, env, basePath,
       frontendModels, backendModels, endpointAuthType, x509CertAlias,
       matchedBy, mtlsEvidenceLevel

6) Optional YAML generation:
   - If --generate-yaml is set:
     - for each matched proxy, run the existing JSON→YAML generator path
     - write to <out>/<env>/<proxyName>/proxy.yaml
     - also store the raw discovery JSON to <out>/<env>/<proxyName>/report.json

7) Docs:
   - Update enterprise-apigeex-applications/docs/apigee-discovery/README.md and proxy-discovery/HOW-IT-WORKS.md with:
     - inventory command usage
     - examples for:
       a) find all proxies supporting oauth on frontend
       b) find all proxies where backend requires client cert (backend contains clientcert)
       c) list proxies with X509CertAlias present (high-confidence mTLS)
     - explain safe defaults: exact match, no aliasing, scope AND across frontend+backend

8) Validation:
   - Add a small unit-test-like script under proxy-discovery/tests/ that:
     - loads a tiny mocked dataset with 3 proxies
     - verifies OR/AND behavior and mtlsEvidenceLevel logic
   - Ensure existing discovery commands still work unchanged.

At the end, output:
- list of files changed
- 3 example commands demonstrating the inventory feature
- confirm no breaking changes to existing YAML keys.
