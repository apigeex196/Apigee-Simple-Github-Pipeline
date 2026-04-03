Review the currently open markdown file and make a final cleanup for the recent template-related documentation changes.

Context:
The goal was to update producer-facing documentation to reflect a single standard proxy template for API producers:
`apigee-default-proxy-v1`

I already made these changes:
- changed `spec.template` guidance to use `apigee-default-proxy-v1`
- updated the minimal YAML example to use `template: apigee-default-proxy-v1`
- removed the multi-template decision tree
- updated the walkthrough to say `Set spec.template to apigee-default-proxy-v1`

Now do a final pass and fix any leftover issues.

Tasks:
1. Find and remove any old or conflicting wording that still suggests API producers should choose from multiple templates.
   Examples of wording to remove or replace:
   - "a valid template name from template-mappings.json"
   - "Choose a template"
   - any remaining multi-template guidance aimed at API producers

2. Keep producer-facing guidance consistent with this rule:
   - API producers should use the standard template `apigee-default-proxy-v1`

3. If `template-mappings.json` is still referenced, make the wording neutral and non-decision-oriented.
   Good direction:
   - "Supported templates are defined in template-mappings.json"
   - do not imply that API producers need to choose among them

4. Keep the wording simple and human-readable.
   Avoid adding extra technical detail.

5. Do not modify unrelated sections.
6. Do not change schema references, repo logic, or code examples outside the relevant template guidance.

Output:
- Return only the revised markdown lines/blocks that need to change
- Keep formatting consistent with the existing document
