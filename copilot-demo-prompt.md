Act as a senior Python engineer and technical demo writer working inside this repository.

I already have a demo guide file:
- LIVE-DEMO-GUIDE.md

Your job is to UPDATE that guide so it becomes a polished, presenter-friendly live demo guide for tomorrow’s meeting.

IMPORTANT
- Do not rewrite randomly.
- Preserve the existing strong parts of the guide.
- Keep the current 3-layer architecture explanation:
  1. INVENTORY = heuristic / non-authoritative
  2. VERIFICATION = OPDK authoritative
  3. MIGRATION = generate artifacts from verified data
- Add the newly implemented Jeremy-requested security summary feature into the demo flow.
- Keep the guide practical for both Windows PowerShell and macOS Terminal.
- Use exact commands where possible.
- If an output is not guaranteed in a local environment, clearly label it as EXPECTED OUTPUT.
- Do not hallucinate files that do not exist in the repo.
- If a file path or CLI flag is uncertain, inspect the code first and use the real implementation.

GOAL
Enhance LIVE-DEMO-GUIDE.md so the demo can show BOTH:
1. the 3-layer architecture refactor
2. the new security summary reporting Jeremy asked for

WHAT TO INCLUDE

1) Keep the current architecture section
Retain the explanation that:
- inventory is heuristic
- verify is authoritative
- extract should use verified data
- unsafe inventory-based migration is blocked or warned

2) Add a new demo section specifically for Jeremy’s feature
Create a new section like:
- Step X - Security Summary Demo
Explain that this shows:
- Proxy Security / Prod Internal
- Proxy Security / Prod External
- Endpoint Security / Prod Internal
- Endpoint Security / Prod External

3) Include the real command
Inspect discover.py and use the real command/flag needed to generate:
- security-summary.json
- security-summary.csv

Show both:
- Windows PowerShell command
- macOS Terminal command

4) Include actual or expected output shape
Show the JSON structure in a compact sample like:
{
  "proxy_security_prod_internal": {
    "OAuth": {
      "count": 5,
      "proxies": [
        {"proxyName": "...", "sysgen": "..."}
      ]
    }
  }
}
Make sure it reflects the real implemented structure.

5) Add presenter notes for the security summary section
Explain what to say during demo:
- “We added a security summary mode”
- “It generates four report groups”
- “Each report contains counts and proxy lists”
- “Results are sorted by sysgen and proxy name”

6) Add honest caveats
Add a “What may be questioned” or “Known caveats” section:
- sysgen may be blank if source data does not contain it
- internal/external classification is currently based on org/env naming conventions
- security type is normalized from auth model fields
Write this carefully and professionally so I can say it confidently in demo.

7) Add a short 2-minute demo script
Create a short presenter script for the full demo:
- show help
- explain architecture
- show inventory/extract safety
- show security summary command
- open security-summary.json
- explain caveats honestly
Keep it concise and natural.

8) Add a “fastest safe demo path” section
Give the safest demo sequence if live systems or credentials are unavailable.
For example:
- show --help
- show verify --help
- show sample verified data
- show security summary generated file
- explain classification caveat
This should minimize risk during live demo.

9) Add a “Jeremy Q&A prep” section
Include likely questions and strong answers for:
- Where does sysgen come from?
- How do you classify internal vs external?
- How do you determine proxy vs endpoint security?
- Is this authoritative or heuristic?
Keep answers short, honest, and senior-level.

10) Preserve markdown quality
Make the final LIVE-DEMO-GUIDE.md:
- easy to scan
- presenter-friendly
- command blocks copy-paste ready
- no fluff
- no vague placeholders if actual values can be derived from code

11) After updating the file
At the end of your response, briefly summarize:
- what sections were added
- what commands were verified from discover.py
- any assumptions that still need validation before demo

QUALITY BAR
- production-quality markdown
- practical
- no fake commands
- no fake outputs presented as actual unless marked expected
- fit for a real enterprise demo tomorrow

Please inspect the existing LIVE-DEMO-GUIDE.md and discover.py first, then update LIVE-DEMO-GUIDE.md directly.
