Read the file "LIVE-DEMO-GUIDE 1.md" in this workspace and generate 2 runnable scripts:

1) demo-run.ps1  (Windows PowerShell)
2) demo-run-mac.sh (macOS bash/zsh compatible)

Goal:
Create scripts that help run the demo commands from the guide in an organized, presenter-friendly way.

Requirements:
- Parse the commands from the markdown file and turn them into executable steps.
- Support the main demo flow from the guide:
  1. discover.py --help
  2. discover.py verify --help
  3. optional display of sample-verified-summary.json
  4. extract command without verification to show blocking behavior
  5. inventory --help
  6. optional security summary command
  7. optional display of output/prod/security-summary.json
- Add a simple menu so I can choose:
  - help-demo
  - architecture-demo
  - security-demo
  - fastest-safe-demo
  - run-all
- Print each command before running it.
- Pause between steps with “Press Enter to continue…” unless a -NoPause or --no-pause flag is passed.
- Use proper platform-specific commands:
  - Windows: python
  - macOS: python3
- Check whether required files exist before running:
  - tool/discover.py
  - sample-verified-summary.json
  - output/prod/security-summary.json
- Check whether Python exists and show a friendly error if not.
- For commands needing env vars:
  - If ESP_APPKEY is missing, skip inventory live run and instead print a warning.
  - If OPDK credentials are missing, do not fail; print that live verify is skipped.
- Do NOT hardcode secrets.
- Add commented placeholders for optional env vars:
  - ESP_APPKEY
  - OPDK_BASE_URL
  - OPDK_ORG
  - OPDK_USER
  - OPDK_PASS
  - OPDK_DISABLE_SSL_VERIFY
- Make the scripts safe:
  - handle errors
  - continue demo where sensible
  - clear console section headers
  - use colored output if practical
- Add a “dry run” mode that only prints commands without executing them.
- Add inline comments explaining each demo section.
- For Windows PowerShell script:
  - name file demo-run.ps1
  - accept parameters like -Mode run-all -DryRun -NoPause
- For macOS script:
  - name file demo-run-mac.sh
  - compatible with bash
  - accept arguments like --mode run-all --dry-run --no-pause
- Also generate a short README section at the end of your response showing:
  - how to run the PowerShell script
  - how to chmod +x and run the macOS script

Important:
- Build the script logic from the commands and flow in "LIVE-DEMO-GUIDE 1.md".
- Prefer the “Fastest Safe Demo Path” when credentials are missing.
- If a command in the guide is example-only and may fail without credentials, wrap it as optional/demo-only.
- Return complete code for both files in separate code blocks.
