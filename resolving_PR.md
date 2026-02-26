
You have access to this repository. I need you to apply Shimmy’s PR feedback:

Remove the workflow changes that make Service Account (SA) retrieval non-blocking (e.g., continue-on-error: true and any conditional skip). Validation must mirror deployment requirements: if PR validation passes, deployment should succeed.

Scope rules

You MAY edit GitHub workflow files under .github/workflows/ only to remove the SA bypass behavior.

Do NOT change any schema files, templates, or other logic.

Do NOT change documentation files except to remove statements that depend on the SA-bypass behavior (if any).

Keep all documentation and demo script improvements otherwise intact.

Tasks

Search all .github/workflows/*.yml and .github/workflows/*.yaml for:

continue-on-error

if: conditions that skip SA checks

steps/actions/scripts that retrieve SA and currently tolerate failures

For every SA retrieval/validation step:

Remove continue-on-error: true

Remove conditional if: that skips SA retrieval/validation

Ensure the step fails the job when SA is missing/invalid (fail-fast)

Ensure PR validation workflows and deploy workflows behave consistently:

PR validation must fail if SA is not configured

Deployment should still require SA (no relaxation)

Verify that the demo path remains possible using SYSGEN788836350_APIGEE-CC (do not hardcode it in workflow; just ensure docs recommend it for demos).

Output requirements

Provide a unified diff of ALL changed files.

Also list which workflows were changed and which lines/steps were responsible for SA validation.

Confirm in one paragraph: “PR validation will now fail if SA is missing, preventing merge-time deployment failures.”

Begin.
