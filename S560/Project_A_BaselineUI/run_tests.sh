#!/usr/bin/env bash
set -e
ROOT_DIR=$(pwd)

# Use the root setup to install dependencies
cd "$ROOT_DIR/.."
./setup.sh
cd "$ROOT_DIR"

mkdir -p logs results screenshots
pytest -q tests/test_pre_visual.py | tee logs/log_pre.txt
pytest -q tests/test_pre_css_assertions.py | tee -a logs/log_pre.txt
pytest -q tests/test_pre_a11y.py | tee -a logs/log_pre.txt

# produce a simple aggregated results.json if not already present
if [ -f results/results_pre.json ]; then
  cp results/results_pre.json results/results_pre.json
fi

echo "Project A tests complete. Results in results/ and screenshots/."
