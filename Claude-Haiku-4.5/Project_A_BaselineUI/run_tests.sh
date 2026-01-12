#!/bin/bash

# Test execution script for Project A - Baseline UI
echo "=== Running Project A - Baseline UI Tests ==="

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Create necessary directories
mkdir -p screenshots
mkdir -p logs
mkdir -p results

# Start logging
exec 1> >(tee logs/log_pre.txt)
exec 2>&1

echo "Starting baseline UI tests at $(date)"

# Run visual tests
echo "Running visual tests..."
cd tests
python test_pre_visual.py

# Run CSS assertion tests
echo "Running CSS assertion tests..."
python test_pre_css_assertions.py

# Run accessibility tests
echo "Running accessibility tests..."
python test_pre_a11y.py

cd ..

echo "Baseline UI tests completed at $(date)"
echo "Results saved to:"
echo "  - screenshots/"
echo "  - logs/log_pre.txt" 
echo "  - results/results_pre.json"
echo "  - results/css_assertions_pre.json"
echo "  - results/a11y_results_pre.json"