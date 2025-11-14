#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR/.."
if [ -f ".venv/bin/activate" ]; then
  . ".venv/bin/activate"
elif [ -f ".venv/Scripts/activate" ]; then
  . ".venv/Scripts/activate"
fi
PORT=8010
python server/server_pre.py &
SERVER_PID=$!
trap 'kill "$SERVER_PID" >/dev/null 2>&1' EXIT
sleep 2
pytest tests/test_pre_visual.py tests/test_pre_css_assertions.py tests/test_pre_a11y.py | tee logs/log_pre.txt
