#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$ROOT"
./Project_A_BaselineUI/run_tests.sh
./Project_B_ImprovedUI/run_tests.sh
cp -f Project_A_BaselineUI/results/results_pre.json results/results_pre.json
cp -f Project_B_ImprovedUI/results/results_post.json results/results_post.json
cp -f Project_A_BaselineUI/screenshots/screenshot_pre_ui.png results/screenshot_pre_ui.png
cp -f Project_B_ImprovedUI/screenshots/screenshot_post_ui.png results/screenshot_post_ui.png
Project_A_BaselineUI/.venv/Scripts/python scripts/generate_diff.py
Project_A_BaselineUI/.venv/Scripts/python scripts/generate_report.py
cp -f results/compare_report.md compare_report.md
