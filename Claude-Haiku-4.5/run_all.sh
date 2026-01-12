#!/bin/bash

# Master execution script - runs both projects and generates comparison report
echo "=== UI/UX Improvement Evaluation - Full Test Suite ==="
echo "Starting complete evaluation at $(date)"

# Clean up previous results
echo "Cleaning up previous results..."
rm -rf results/*
mkdir -p results

# Run Project A - Baseline UI tests
echo ""
echo "=== PHASE 1: Running Baseline UI Tests ==="
cd Project_A_BaselineUI
chmod +x run_tests.sh
./run_tests.sh
cd ..

# Copy baseline results to main results directory
echo "Copying baseline results..."
cp Project_A_BaselineUI/screenshots/screenshot_pre_ui.png results/ 2>/dev/null || echo "Screenshot not found"
cp Project_A_BaselineUI/results/*.json results/ 2>/dev/null || echo "Baseline results not found"
cp Project_A_BaselineUI/logs/log_pre.txt results/ 2>/dev/null || echo "Baseline log not found"

# Run Project B - Improved UI tests  
echo ""
echo "=== PHASE 2: Running Improved UI Tests ==="
cd Project_B_ImprovedUI
chmod +x run_tests.sh
./run_tests.sh
cd ..

# Copy improved results to main results directory
echo "Copying improved results..."
cp Project_B_ImprovedUI/screenshots/screenshot_post_ui.png results/ 2>/dev/null || echo "Screenshot not found"
cp Project_B_ImprovedUI/results/*.json results/ 2>/dev/null || echo "Improved results not found"  
cp Project_B_ImprovedUI/logs/log_post.txt results/ 2>/dev/null || echo "Improved log not found"

# Generate comparison report
echo ""
echo "=== PHASE 3: Generating Comparison Report ==="
python generate_comparison_report.py

echo ""
echo "=== EVALUATION COMPLETE ==="
echo "Full evaluation completed at $(date)"
echo ""
echo "Results available in:"
echo "  - results/compare_report.md (Main comparison report)"
echo "  - results/screenshot_pre_ui.png (Baseline UI)"
echo "  - results/screenshot_post_ui.png (Improved UI)"
echo "  - results/*.json (Detailed test results)"
echo "  - results/log_*.txt (Test execution logs)"
echo ""
echo "To view the comparison report:"
echo "  cat results/compare_report.md"