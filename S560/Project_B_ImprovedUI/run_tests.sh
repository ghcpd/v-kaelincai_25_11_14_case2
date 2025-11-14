#!/usr/bin/env bash
set -e
ROOT_DIR=$(pwd)

# Use top-level setup
cd "$ROOT_DIR/.."
./setup.sh
cd "$ROOT_DIR"

mkdir -p logs results screenshots
pytest -q tests/test_post_visual.py | tee logs/log_post.txt
pytest -q tests/test_post_css_assertions.py | tee -a logs/log_post.txt
pytest -q tests/test_post_a11y.py | tee -a logs/log_post.txt

echo "Project B tests complete. Results in results/ and screenshots/."
