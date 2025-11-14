#!/usr/bin/env bash
set -e
# Run baseline
pushd Project_A_BaselineUI
bash run_tests.sh
popd
# Run improved
pushd Project_B_ImprovedUI
bash run_tests.sh
popd
# Generate aggregate report
python scripts/generate_report.py

echo "All tests complete. See results/compare_report.md"