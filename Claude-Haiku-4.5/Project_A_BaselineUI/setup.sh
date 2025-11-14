#!/bin/bash

# Setup script for Project A - Baseline UI
echo "Setting up Project A - Baseline UI..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
pip install -r requirements.txt

# Install playwright browsers
playwright install chromium

echo "Project A setup complete!"
echo "To run tests: ./run_tests.sh"