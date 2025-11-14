#!/bin/bash

# Test execution script for Project B - Improved UI
echo "=== Running Project B - Improved UI Tests ==="

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
exec 1> >(tee logs/log_post.txt)
exec 2>&1

echo "Starting improved UI tests at $(date)"

# Run visual tests
echo "Running visual tests..."
cd tests
python test_post_visual.py

# Run CSS assertion tests
echo "Running CSS assertion tests..."
python test_post_css_assertions.py

# Run accessibility tests
echo "Running accessibility tests..."
python test_post_a11y.py

cd ..

echo "Improved UI tests completed at $(date)"
echo "Results saved to:"
echo "  - screenshots/"
echo "  - logs/log_post.txt"
echo "  - results/results_post.json"
echo "  - results/css_assertions_post.json" 
echo "  - results/a11y_results_post.json"