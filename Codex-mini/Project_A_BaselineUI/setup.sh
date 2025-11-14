#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
if [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  . ".venv/bin/activate"
elif [ -f ".venv/Scripts/activate" ]; then
  # shellcheck disable=SC1091
  . ".venv/Scripts/activate"
fi
pip install -r requirements.txt
python -m playwright install
