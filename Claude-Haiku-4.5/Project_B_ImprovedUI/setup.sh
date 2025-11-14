#!/bin/bash

# Setup script for Project B - Improved UI  
echo "Setting up Project B - Improved UI..."

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

echo "Project B setup complete!"
echo "To run tests: ./run_tests.sh"