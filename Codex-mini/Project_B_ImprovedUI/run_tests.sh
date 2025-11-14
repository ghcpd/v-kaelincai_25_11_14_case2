#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR/.."
if [ -f ".venv/bin/activate" ]; then
  . ".venv/bin/activate"
elif [ -f ".venv/Scripts/activate" ]; then
  . ".venv/Scripts/activate"
fi
PORT=8020
python server/server_post.py &
SERVER_PID=$!
trap 'kill "$SERVER_PID" >/dev/null 2>&1' EXIT
sleep 2
pytest tests/test_post_visual.py tests/test_post_css_assertions.py tests/test_post_a11y.py | tee logs/log_post.txt
