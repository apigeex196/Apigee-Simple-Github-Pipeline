# API Producer Core Guide

Audience: API producer teams onboarding to Apigee X via this applications repository.
Scope: Author proxies/products, validate with schemas, deploy with workflows, and test.

Think of this repository as the source of truth for API configuration, where Git changes drive Apigee deployments.

## Intended Audience

This guide is intended for API producer teams who:
- Own backend services
- Need to expose APIs via Apigee X
- Use this repository to manage API configurations

This guide is NOT intended for:
- Platform engineers managing templates, shared flows, or CI/CD workflows

---

## Overview

This repository uses a stage-based folder structure for API proxy and product deployments:
- You work in your SYSGEN folder: `SYSGEN<9digits>_<MAL_ACRONYM>/`
- Proxy YAMLs live under `(dev|test|prod)/proxies/`
- Product YAMLs live under `(dev|test|prod)/products/`
- Workflows validate schema on PR and deploy on merge to `main`
- Promotion: dev → test → prod by copying/updating YAMLs for each stage

**Workflow Triggers:**
- Proxy validation/deploy: `SYSGEN*_*/dev/proxies/**/*.yaml`, `SYSGEN*_*/test/proxies/**/*.yaml`, `SYSGEN*_*/prod/proxies/**/*.yaml`
- Product validation/deploy: `SYSGEN*_*/(dev|test|prod)/products/*.yaml` and `global/(dev|test|prod)/products/*.yaml`
- Schema validation requires `kind: ApiProxy` or `kind: ApiProduct`

This section explains the repository structure and deployment behavior. For a conceptual understanding of how this repository is used by API producers, see the next section.

## What This Repository Does

This repository enables API producer teams to publish APIs into Apigee X using a Git-based workflow.

Instead of manually configuring APIs in Apigee UI, producers define API proxies and products using YAML files in this repository. These configurations are validated through pull requests and automatically deployed to Apigee environments via CI/CD workflows.

## Apigee Basics (Quick Concepts)

### API Proxy
An API proxy is a gateway layer in Apigee that sits between clients and backend services, handling routing, security, and policies.

### API Product
An API product is a bundle of APIs that can be exposed to consumers with access control, quotas, and scopes.

### Environment
An environment represents a deployment stage such as dev, test, or prod.

### Shared Flows
Shared flows are reusable policy components managed by the platform team and used by proxy templates.

## Responsibilities

### API Producer Responsibilities
- Define API proxies using YAML
- Define API products (if required)
- Maintain OpenAPI specifications (optional)
- Raise pull requests for changes
- Validate and test APIs after deployment

### Platform Responsibilities
- Maintain proxy templates
- Manage shared flows and policies
- Maintain CI/CD workflows
- Provision service accounts and environments

---

## Repo Layout (SYSGEN Structure)

**Proxy paths:**
```
SYSGEN<9digits>_<MAL_ACRONYM>/(dev|test|prod)/proxies/(public|private)/<env-name>/*.yaml
```
Example: `SYSGEN788836350_APIGEE-CC/test/proxies/private/test1/proxy.yaml`

**Product paths:**
```
SYSGEN<9digits>_<MAL_ACRONYM>/(dev|test|prod)/products/*.yaml
global/(dev|test|prod)/products/*.yaml
```
Examples:
- `SYSGEN788836350_APIGEE-CC/test/products/SYSGEN788836350-my-product.yaml`
- `global/test/products/shared-product.yaml`

**Folder structure example:**
```
SYSGEN788836350_APIGEE-CC/
  test/
    proxies/
      private/
        test1/
          proxy.yaml
          your-openapi.yaml
    products/
      SYSGEN788836350-my-product.yaml
  dev/
    proxies/
      private/
        dev1/
          proxy.yaml
global/
  test/
    products/
      shared-product.yaml
```

**Notes:**
- Filenames can be any `*.yaml`; `proxy.yaml` is a recommended convention
- OAS files live in the same directory as the proxy YAML
- Workflows trigger on changes matching the path patterns above

---

## Getting Started

**Prerequisites:**
- Access to this repository (read/write permissions)
- A SYSGEN code (e.g., `SYSGEN788836350`) assigned by platform governance
- Service accounts provisioned per SYSGEN per stage (dev, test, prod)
- Tools: Git, GitHub CLI, Python 3.10+ (optional: Node.js for local validation with `ajv-cli`)

**Access & Provisioning:**
- GitHub repo access: request through your internal access management system
- SYSGEN code: assigned by platform governance; include application name, team contact, and business justification
- Service accounts: provisioned per SYSGEN per stage with IAM permissions for Apigee deployment, Secret Manager, and Cloud Storage
- Follow access and escalation guidance in [docs/repository-configuration.md](repository-configuration.md)

---

## Quickstart (Windows)

Set variables:
```powershell
$sysgen = "SYSGEN788836350"
$team = "APIGEE-CC"
$stage = "test"        # dev | test | prod
$visibility = "private" # public | private
$envName = "test1"
$project = "$sysgen-E2E-TEST-BASIC"
$root = "$sysgen`_$team/$stage/proxies/$visibility/$envName"
```

Create proxy YAML:
```powershell
New-Item -ItemType Directory -Force "$root" | Out-Null
Set-Content "$root/proxy.yaml" @"
apiVersion: apienable.lumen.com/v1beta1
kind: ApiProxy
metadata:
  name: $project
  description: "Basic proxy example"
  labels:
    sysgen: $sysgen
    taxonomy: /Test/v1/E2E
spec:
  template: oauth-proxy-oauth-backend
  routing:
    path: /sysgen788836350/e2e-test-basic/v1
    target: https://httpbin.org
    rewritePath: /anything
    timeout: 35
"@
```

Validate locally (requires Node.js and `ajv-cli`):
```powershell
yq eval -o=json '.' "$root/proxy.yaml" > proxy.json
npm install -g ajv-cli ajv-formats
ajv validate -s apiproxy.schema.json -d proxy.json --spec=draft7
```

Commit, open a PR, and merge to trigger deployment.

## End-to-End Workflow

1. Create or update proxy YAML under the appropriate stage folder
2. Create or update product YAML (if required)
3. Commit changes to a feature branch
4. Raise a Pull Request
5. Validation workflows run automatically
6. Fix validation issues if any
7. Merge Pull Request into main
8. Deployment workflow triggers automatically
9. API is deployed to the corresponding Apigee environment
10. Promote configuration to next stage (dev → test → prod)

---

## Authoring Proxies

**Required fields:**
- `metadata.name`: SYSGEN-prefixed (e.g., `SYSGEN788836350-my-api`), must match pattern `SYSGEN[0-9]{9}-*`
- `metadata.labels.sysgen`: your SYSGEN code
- `metadata.labels.taxonomy`: API taxonomy (e.g., `/Channel/v1/Portal`)
- `spec.template`: a valid template name from [../template-mappings.json](../template-mappings.json)
- `spec.routing.path`: base path (e.g., `/sysgen788836350/my-api/v1`)
- `spec.routing.target`: backend URL

**Naming conventions:**
- Prefer kebab-case: `SYSGEN788836350-my_api`
- Avoid trailing slashes in routing paths
- Do not use `targetAudience` (not in schema); use labels instead

**Schema reference:** [../apiproxy.schema.json](../apiproxy.schema.json)

**Minimal example:**
```yaml
apiVersion: apienable.lumen.com/v1beta1
kind: ApiProxy
metadata:
  name: SYSGEN788836350-my-api
  description: "Example proxy"
  labels:
    sysgen: SYSGEN788836350
    taxonomy: /Channel/v1/Portal
spec:
  template: oauth-proxy-oauth-backend
  routing:
    path: /sysgen788836350/my-api/v1
    target: https://httpbin.org
```

**Template decision tree:**
| Template | Use when |
| --- | --- |
| `oauth-proxy-oauth-backend` | OAuth token introspection via backend |
| `jwt-proxy-ahpt-backend` | Local JWT verification (no introspection) |
| `oauth-proxy-jwt-backend` | Both OAuth and JWT required |
| `jwt-oauth-proxy-ahpt-backend` | Combined JWT+OAuth for AHPT backend |
| No‑Target (utility) | Stub/no backend yet |

Reference: [../template-mappings.json](../template-mappings.json)

**First proxy walkthrough:**
1. Choose a template and set `spec.template` in your proxy YAML
2. Create proxy YAML under `SYSGEN<9digits>_<MAL_ACRONYM>/(dev|test|prod)/proxies/(public|private)/<env-name>/proxy.yaml`
3. Open a PR; fix validation failures (schema, naming, template)
4. Merge to `main`; deployment runs automatically for the target stage
5. Promote by copying YAML to next stage folder (dev → test → prod) and updating stage-specific values

---

## OAS Validation (Optional)

**Enable OAS linting:**
Add under `spec` in your proxy YAML:
```yaml
oasValidation:
  enabled: true
  oasResource: oas://your-openapi.yaml
```

**File placement:**
Place your OAS file in the same directory as your proxy YAML:
```
SYSGEN788836350_APIGEE-CC/test/proxies/private/test1/
  proxy.yaml
  your-openapi.yaml
```

**Supported specs:** OpenAPI 3.x (preferred), Swagger 2.0

**Build behavior:** Workflows inject the OAS file into `apiproxy/resources/oas/` so policies can resolve `oas://`

**Minimal OpenAPI 3 example:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
paths:
  /health:
    get:
      responses:
        '200':
          description: OK
```

**Common validation failures:**
- OAS file not found → verify filename and `oas://` reference; ensure it is committed
- Missing required fields → ensure `info`, `paths`, and response objects exist
- Format errors → run `npx @redocly/openapi-cli@latest lint <file>` locally

For details: [docs/OAS-VALIDATION.md](OAS-VALIDATION.md)

---

## API Products

**Overview:**
Products are deployed from YAML files committed under the products paths. Workflows validate and deploy any Product YAML found under:
- `SYSGEN<9digits>_<MAL_ACRONYM>/(dev|test|prod)/products/*.yaml`
- `global/(dev|test|prod)/products/*.yaml`

If no Product YAML is provided, product behavior depends on platform defaults (not workflow-driven).

**When to create a custom product:**
- Manual approval workflows
- Custom quotas
- OAuth scope control
- Multiple proxies under one product
- Fine-grained operation-level access

**Product YAML location:**
- SYSGEN-specific: `SYSGEN788836350_APIGEE-CC/test/products/SYSGEN788836350-my-product.yaml`
- Global shared: `global/test/products/shared-product.yaml`

**Linking proxies:**
Set `spec.proxies[].name` to your SYSGEN-prefixed proxy name (e.g., `SYSGEN788836350-my-api`)

**Safe to modify:**
- `spec.quota` (rate limiting)
- `spec.scopes` (OAuth scopes)
- `spec.approval` (`auto` or `manual`)
- `spec.access` (`public`, `private`, `internal`)
- `spec.proxies` (proxy list and operations)
- `spec.attributes` (custom metadata)

**Do NOT modify:**
- `apiVersion` (must be `v1`)
- `kind` (must be `ApiProduct`)
- `metadata.sysgen` (enforced pattern)
- Internal platform metadata keys

**Quota fields:**
- `limit`: number of requests per interval (e.g., `1000`)
- `interval`: how many time units (e.g., `1`)
- `timeUnit`: `minute`, `hour`, or `day`

Example: `limit: 1000`, `interval: 1`, `timeUnit: minute` = 1000 requests per minute

**Schema reference:** [../apiproduct.schema.json](../apiproduct.schema.json)

**Minimal example:**
```yaml
apiVersion: v1
kind: ApiProduct
metadata:
  name: SYSGEN788836350-my-product
  description: "Product for my APIs"
  sysgen: SYSGEN788836350
  owner: api-team@example.com
  approvedBySRB: true
spec:
  approval: auto
  access: public
  environments:
    - apicc-dev1
  proxies:
    - name: SYSGEN788836350-my-api
      operations:
        - path: /sysgen788836350/my-api/v1/health
          methods:
            - GET
  quota:
    limit: 1000
    interval: 1
    timeUnit: minute
  scopes:
    - read
    - write
  attributes:
    team: api-producers
```

**Promotion:**
1. Copy product file to next stage folder (dev → test → prod)
2. Update `spec.environments` to target environment(s)
3. Merge and verify deployment in target stage

For failure modes: [API-PRODUCER-FAILURE-MODES.md](API-PRODUCER-FAILURE-MODES.md)

---

## Before You Raise a PR

- Ensure YAML follows schema (ApiProxy / ApiProduct)
- Verify folder structure matches the `SYSGEN<9digits>_<MAL_ACRONYM>` stage layout
- Validate naming conventions (SYSGEN prefix plus MAL acronym)
- Confirm the chosen template exists in `template-mappings.json`
- Ensure the OAS file is present when `oasValidation.enabled` is true
- Test locally (ajv-cli, Redocly OpenAPI CLI, etc.) if tooling is available

## Validation Expectations

All changes must pass validation checks during pull request:

- YAML schema validation (ApiProxy / ApiProduct)
- Folder structure validation
- Naming convention validation (SYSGEN prefix, MAL acronym)
- Template validation

Pull requests cannot be merged until all validations pass.

## Validation & Deployment Workflows

**Workflow behavior:**
- Validation runs on PRs
- Deployment runs after merge to `main`
- Triggers: files matching `SYSGEN*_*/(dev|test|prod)/(proxies/**|products)/*.yaml` and `global/(dev|test|prod)/products/*.yaml`
- Schema validation requires `kind: ApiProxy` or `kind: ApiProduct`

**Typical flow:**
1. Create branch, add proxy/product YAML
2. Open PR → validation checks (schema, apigeelint, naming, service account existence)
3. Merge PR → deploy to target stage

**Environment approvals:**
- dev: auto-deploy on merge
- test: may require approval (GitHub Environments)
- prod: requires platform approvals and wait timer

**Workflow references:**
- [workflows/validate-proxy.md](workflows/validate-proxy.md)
- [workflows/validate-product.md](workflows/validate-product.md)
- [../.github/workflows/validate-product.yml](../.github/workflows/validate-product.yml)
- [../.github/workflows/deploy-products.yml](../.github/workflows/deploy-products.yml)

**Local validation (recommended):**
```powershell
# Convert YAML to JSON and validate with ajv-cli
yq eval -o=json '.' "$root/proxy.yaml" > proxy.json
npm install -g ajv-cli ajv-formats
ajv validate -s apiproxy.schema.json -d proxy.json --spec=draft7
```

For products: validate against [../apiproduct.schema.json](../apiproduct.schema.json)

---

## Promotion Guidance (dev → test → prod)

**Process:**
- Copy YAML to destination stage folder
- Update stage-specific fields (environment names, service account, labels)
- Keep structure consistent across stages; only stage-specific values differ
- Workflows trigger on any `*.yaml` under these paths; `proxy.yaml` is the recommended naming convention

**Example structure:**
```text
SYSGEN788836350_APIGEE-CC/
  dev/proxies/private/dev1/proxy.yaml
  test/proxies/private/test1/proxy.yaml
  prod/proxies/private/prod1/proxy.yaml
```

**Service accounts & secrets:**
 - Platform provisions service accounts per SYSGEN per stage
 - See guidance: [planning/SECRETS-INVENTORY-CHECKLIST.md](../planning/SECRETS-INVENTORY-CHECKLIST.md), [docs/repository-configuration.md](repository-configuration.md)

---

## Demo and Reference Material

Refer to:
- Demo recordings provided by the platform team (supporting scripts live in `../docs/demo/DEMO-CHEATSHEET.md` and `../docs/demo/DEMO-SCRIPTS-README.md`)
- Example pull requests in this repository that touch `SYSGEN*/(dev|test|prod)/proxies` and `SYSGEN*/(dev|test|prod)/products` to see real changesets
- Testing and validation guides under the docs folder (`../docs/API-PRODUCER-FAILURE-MODES.md`, `../docs/API-PRODUCER-LIVE-DEMO.md`)

## Testing

**Expectations and steps:**
- [TESTING-CHECKLIST.md](../TESTING-CHECKLIST.md)
- [docs/E2E-TESTING-DPEAPI-18719.md](E2E-TESTING-DPEAPI-18719.md)
- Bruno collections: [tests/bruno-collections/apigee-e2e-tests/README.md](../tests/bruno-collections/apigee-e2e-tests/README.md)

**Non-platform engineer test:**
Use this checklist to validate onboarding without platform assistance:
- Name / Team / Date
- SYSGEN used (e.g., SYSGEN788836350)
- Proxy name (e.g., SYSGEN788836350-my-api)
- Time to first deploy (target: < 30 minutes)
- Any platform help needed? (Yes/No — describe if Yes)
- Links to PR(s) as evidence

**Reference materials:**
- [docs/demo/DEMO-REFERENCE.md](../docs/demo/DEMO-REFERENCE.md)
- [docs/demo/PLATFORM-DEMO-PRESENTATION.md](../docs/demo/PLATFORM-DEMO-PRESENTATION.md)
- [README.md](../README.md)

---

## Common Producer Mistakes

- Incorrect folder path (wrong stage or structure)
- Invalid SYSGEN naming pattern on `metadata.name`
- Missing or incorrect `kind` field (must be `ApiProxy` or `ApiProduct`)
- Using unsupported template names (missing from `template-mappings.json`)
- Missing OAS file when `oasValidation.enabled` is true
- Incorrect environment configuration (stage vs. Apigee org/env mapping)
- Product not linked to proxy correctly (`spec.proxies[].name`)

## Troubleshooting / Shared Flows

**Troubleshooting:**
- Undeploy/redeploy: [docs/PROXY-UNDEPLOY.md](PROXY-UNDEPLOY.md)
- General issues: [docs/archive/TROUBLESHOOTING.md](archive/TROUBLESHOOTING.md)
- Failure modes: [API-PRODUCER-FAILURE-MODES.md](API-PRODUCER-FAILURE-MODES.md)

**Shared flows:**
- Templates include FlowCallout policies referencing shared flows managed by the platform team
- Workflows do not validate shared flow existence; deployments may succeed even if missing
- Expected symptom: runtime faults (e.g., "Shared flow not found")
- Coordinate with platform team to ensure shared flows are deployed before go-live

**Environment notes:**
- Internal (`apicc-*`) vs external (`ext-apicc-*`) environments: choose based on consumer location
- External environments may have additional controls

---

## References

**Schemas:**
- [../apiproxy.schema.json](../apiproxy.schema.json)
- [../apiproduct.schema.json](../apiproduct.schema.json)

**Workflows:**
- [workflows/validate-proxy.md](workflows/validate-proxy.md)
- [workflows/validate-product.md](workflows/validate-product.md)

**Testing:**
- [../TESTING-CHECKLIST.md](../TESTING-CHECKLIST.md)
- [E2E-TESTING-DPEAPI-18719.md](E2E-TESTING-DPEAPI-18719.md)

**Repository config:**
- [repository-configuration.md](repository-configuration.md)

**Templates:**
- [../template-mappings.json](../template-mappings.json)
