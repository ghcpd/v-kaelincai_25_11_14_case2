# Task List Visual Redesign Evaluation

This workspace contains two projects that demonstrate a before/after UI redesign for a task-list app. It includes interactive frontends, automated visual/CSS/accessibility tests, and a report generator.

Run a full workflow with: `bash run_all.sh` (Linux/macOS/Git Bash) or `.\run_all.ps1` (PowerShell). The scripts create virtual environments, install dependencies, start servers, run tests, capture screenshots and produce a compare report.

Folders:
- Project_A_BaselineUI — baseline dense UI
- Project_B_ImprovedUI — improved UI
- shared — test_data.json used by both projects
- scripts — tools for generating and aggregating reports
- results — aggregated outputs

See `scripts/generate_report.py` for report generation logic.
