#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
# Start server in background
PORT=8002
python server/server_post.py &
SPID=$!
sleep 1
python -u tests/run_tests.py
kill $SPID

echo "Tests complete. Results -> results/results_post.json"