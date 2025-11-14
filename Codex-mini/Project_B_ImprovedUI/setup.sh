#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
if [ -f ".venv/bin/activate" ]; then
  . ".venv/bin/activate"
elif [ -f ".venv/Scripts/activate" ]; then
  . ".venv/Scripts/activate"
fi
pip install -r requirements.txt
python -m playwright install
