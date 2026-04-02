You are editing the currently open markdown document.

Focus ONLY on the "Quickstart (Windows)" section.

There are two PR comments:

1) "This section could use some more instructions on how to set those..."
2) "This section is confusing. It looks like you're mixing commands and yaml text... Is that example even needed here?"

----------------------------------------

GOAL:

Make this section:
- Human-readable
- Step-by-step actionable
- Minimal (true Quickstart)
- Free of confusion

----------------------------------------

REQUIRED CHANGES:

### 1. VARIABLE SETUP (Fix clarity + intent)

Before the variable block:

- Add a short explanation:
  - What these variables are used for (building paths and names)
  - That they must be set before running commands
  - That they are set in a PowerShell session

- Clearly list ALL variables:
  $sysgen, $team, $stage, $visibility, $envName, $project, $root

- Add:
  - Note: variables are temporary unless added as Windows User Environment Variables
  - Microsoft Docs link for PowerShell variables

----------------------------------------

### 2. SIMPLIFY QUICKSTART (CRITICAL)

Rewrite Quickstart as a **clean sequence of steps**:

Step 1: Set variables  
Step 2: Create folder  
Step 3: Create proxy.yaml file  
Step 4: Paste YAML  
Step 5: Commit → PR → Merge  

- No extra explanation blocks
- No branching paths
- No optional steps

----------------------------------------

### 3. REMOVE COMMAND + YAML MIXING

- REMOVE usage of:
  Set-Content @"...yaml..."

- Instead:
  - Show YAML as a standalone ```yaml block
  - Add instruction:
    "Save this as proxy.yaml in the path defined above"

----------------------------------------

### 4. REMOVE OR RELOCATE VALIDATION

- REMOVE "Validate locally" from Quickstart
- Create new section:

## Optional: Local Validation

- Move all validation commands there
- Keep content unchanged

----------------------------------------

### 5. REMOVE REDUNDANT / CONFUSING EXAMPLES

- If multiple ways exist to do the same thing → keep only ONE clear method
- Prefer manual file creation over scripted generation

----------------------------------------

### 6. KEEP STRICT BOUNDARIES

DO NOT:
- Modify technical logic
- Change YAML structure
- Change paths
- Add new concepts

----------------------------------------

OUTPUT:

Return ONLY:
1. Updated "Quickstart (Windows)" section
2. New "Optional: Local Validation" section

Ensure:
- Clean formatting
- Clear steps
- Beginner-friendly tone
- No mixing of concepts
