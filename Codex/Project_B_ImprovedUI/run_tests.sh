#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

./setup.sh
# shellcheck disable=SC1090
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate

python server/server_post.py >logs/server_post.log 2>&1 &
SERVER_PID=$!
cleanup() {
  if ps -p $SERVER_PID >/dev/null 2>&1; then
    kill $SERVER_PID
  fi
}
trap cleanup EXIT

for _ in {1..20}; do
  if curl -s http://127.0.0.1:5002/healthz >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done

python -m tests.run_suite_post
