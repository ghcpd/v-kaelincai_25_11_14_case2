#!/usr/bin/env bash
set -euo pipefail
VENV_DIR=".venv"
PYTHON_BIN="python3"
if command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
fi
if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1090
source "$VENV_DIR"/bin/activate 2>/dev/null || source "$VENV_DIR"/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install --with-deps chromium
