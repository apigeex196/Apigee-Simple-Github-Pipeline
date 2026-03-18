Act as a senior Python engineer and technical documentation writer working inside this repository.

Your job is to create a new markdown file named:

IMPLEMENTATION-GUIDE-JEREMY-SECURITY-SUMMARY.md

IMPORTANT
Use the Jeremy comments below as the source requirement. Do not say you do not know Jeremy’s comments. They are provided here explicitly.

JEREMY COMMENTS / REQUIREMENT
“Can you modify that extract tool… you probably have logic already… feature for it is to get a count of all the different proxy and endpoint security types, both for internal and external prod. Simple count and a list of security types / security models being used. List out both the proxy names and the sys gens, preferably sorted by sys gen. Two lists for proxy security and endpoint security, another for Prod Internal and Prod External — the four lists total.”

GOAL
Create a clear implementation guide that proves the above Jeremy-requested security-summary feature has been implemented in the codebase, aligned point-by-point with his comments.

CRITICAL RULES
- Inspect the real code first, especially discover.py and any related tests.
- Base the guide on actual implementation, not assumptions.
- Be honest about what is fully implemented versus what is heuristic or data-dependent.
- Do not claim anything is authoritative unless the code clearly supports that.
- If some requirement is only partially satisfied, say so clearly.
- Keep the tone professional and suitable for technical review.

FILE TO CREATE
IMPLEMENTATION-GUIDE-JEREMY-SECURITY-SUMMARY.md

REQUIRED STRUCTURE

1) Title and Purpose
Explain that this document maps Jeremy’s requested feature to the current implementation.

2) Jeremy Request Summary
Quote or restate the requirement in clean bullet points:
- count different proxy security types
- count different endpoint security types
- internal and external prod views
- list proxy names and sys gens
- sort by sys gen
- four total report groups

3) Point-by-Point Implementation Matrix
Create a markdown table:

| Jeremy Requirement | Status | Where Implemented | Notes |

Allowed status values:
- Implemented
- Implemented with caveat
- Partially implemented
- Not implemented

Fill this table from actual code inspection.

4) Implementation Details
Create sections for:

## CLI Surface
- show the real command/flag added for this feature

## Report Groups Generated
- show the exact four group keys used in output JSON

## Proxy Security Derivation
- explain how proxy security type is derived in code

## Endpoint Security Derivation
- explain how endpoint security type is derived in code

## Internal vs External Classification
- explain exactly how classification works in code
- clearly state if it depends on org/env naming conventions

## Sysgen Handling
- explain where sysgen comes from in code
- explain whether it can be blank
- explain whether it may be inferred from proxy naming patterns

## Sorting
- explain how sorting is done in code

## Output Files
- mention generated files such as security-summary.json and security-summary.csv

5) Code References
Create a section that lists the real functions / areas used as evidence, such as:
- normalize_proxy_record
- classify_exposure
- get_security_type_from_models
- generate_security_summary
- write_security_summary_json
- write_security_summary_csv

For each one, briefly explain its purpose.

6) Test Coverage
If tests exist, mention the real test file(s) and what they verify.

7) Example Output
Provide a compact example JSON structure that matches the real output format.

8) Known Caveats
Be explicit and honest. Call out things such as:
- internal/external classification may be convention-based
- sysgen may be blank if source data does not contain it
- security type may be reduced to a primary normalized label
- this is reporting-oriented and not the same as authoritative migration verification

9) Conclusion
Write a reviewer-ready conclusion stating whether Jeremy’s requirement is:
- implemented
- implemented with caveats
- or partially implemented

The conclusion should be technically defensible, not marketing language.

10) Optional Demo Section
Add a short “How to Demo This” section with:
- the command to run
- what file to open
- what to say briefly

STYLE
- professional markdown
- concise but complete
- no fluff
- no fake commands
- no hallucinated files
- no unsupported claims

At the end of your response, briefly summarize:
- which Jeremy points are fully implemented
- which ones have caveats
- which files/functions were used as evidence

Please inspect the current repository and write IMPLEMENTATION-GUIDE-JEREMY-SECURITY-SUMMARY.md directly.
