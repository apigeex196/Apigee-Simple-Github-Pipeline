Edit the currently open markdown document in place.

This file is the API Producer core guide in the repo. It has already been cleaned up for template guidance and broken links, but it still needs a structural update based on PR feedback.

PR feedback to address:
- Re-proof read in rich view mode
- Make the organization and instruction flow human-readable
- Align the repo doc with the SharePoint QuickStart “Steps” structure
- Most users will read the quick start first, then come to the repo for details
- The repo quickstart file is redundant; SharePoint should be the primary quick start
- The repo doc should provide more detailed information for each step, plus troubleshooting and FAQs

Goal:
Turn this document into a step-aligned detailed reference that fits the SharePoint QuickStart structure, without rewriting all technical content.

What to change:

1. Add a new section near the top, after the introduction / audience / overview area:

## Quick Start (Recommended)

Add a short paragraph saying:
- For step-by-step onboarding, use the SharePoint QuickStart guide
- This repository document is the detailed technical reference for the same flow

Do not invent a SharePoint URL if one is not already present in the file. Use placeholder text like:
`[Apigee X Migration - API Producer QuickStart Guide](SHAREPOINT_LINK)`
only if needed.

2. Add a new section:

## Steps Overview

Include this ordered list:
1. Request MAL onboarding
2. Understand your MAL folder
3. Create your first proxy
4. Validate your proxy
5. Deploy your proxy

Add one short line saying this document provides detailed guidance for those steps.

3. Reorganize the existing document by adding step headings that align to the SharePoint flow. Do NOT rewrite the technical content unless needed for transitions.

At minimum:
- Add `## Step 3: Create Your First Proxy` before the current proxy creation / quickstart content
- Add `## Step 4: Validate Your Proxy` before local validation / OAS validation / validation expectations content
- Add `## Step 5: Deploy Your Proxy` before deployment workflow / promotion guidance content

4. Keep existing detailed reference sections, but place them under the appropriate step flow where reasonable.

5. Add brief transition text under each new step heading so the flow reads naturally for humans.

6. Do NOT change:
- YAML examples unless needed for heading placement
- template guidance already updated to `apigee-default-proxy-v1`
- schema links
- workflow links
- product content
- troubleshooting content

7. Keep the document as a detailed reference, not a short tutorial.

8. Make sure the markdown still reads well in rich view:
- clear headings
- logical order
- minimal repetition
- easy to scan

9. Output the edited markdown directly in the file. Do not just explain changes.

10. Also check whether the repo quickstart file name `API-PRODUCER-QUICKSTART.md` is referenced inside this document. If it is referenced, replace that wording so the SharePoint guide is presented as the primary quick start and this file as the detailed reference.

Important:
- Preserve existing content as much as possible
- Focus on restructuring and flow
- Make the changes directly, not just suggestions
