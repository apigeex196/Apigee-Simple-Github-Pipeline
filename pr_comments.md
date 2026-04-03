You are editing the currently open markdown file for the API Producer guide.

Focus ONLY on the sections in "Authoring Proxies" that discuss `spec.template`, the minimal example, the template decision tree, and the first proxy walkthrough.

Reviewer comments say:
"Needs to be updated to reflect the 'single proxy template'."

Important context from the current repository:
- The repo still technically supports multiple templates in `template-mappings.json` and `apiproxy.schema.json`
- BUT this documentation should present a single standard template for API producers
- Do NOT change repository code, schema references, or template-mappings.json
- Only update the documentation guidance

Your task:
1. Update all producer-facing guidance to use the single standard proxy template:
   `apigee-default-proxy-v1`

2. In the "Required fields" section, change the description of `spec.template` so it no longer says to choose from multiple templates. Replace it with guidance to use:
   `apigee-default-proxy-v1`

3. In the minimal YAML example, replace:
   `template: oauth-proxy-oauth-backend`
   with:
   `template: apigee-default-proxy-v1`

4. Remove the entire "Template decision tree" section or replace it with a short statement that API producers should use the standard template:
   `apigee-default-proxy-v1`

5. In the "First proxy walkthrough", replace wording like:
   "Choose a template and set spec.template ..."
   with direct wording like:
   "Set spec.template to `apigee-default-proxy-v1` ..."

6. Keep any reference to `template-mappings.json` only if needed as a neutral reference, but do NOT present it as a producer decision point.

7. Do NOT say that only one template exists in the repository.
8. Do NOT mention all alternative template names.
9. Do NOT rewrite unrelated sections.

Output:
- Return only the revised markdown blocks that should be changed
- Preserve formatting style of the current document
- Keep wording simple, human-readable, and suitable for API producers
