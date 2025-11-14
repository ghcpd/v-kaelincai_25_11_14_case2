python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install
# Start server
$port=8002
Start-Process -NoNewWindow -FilePath python -ArgumentList "server/server_post.py"
Start-Sleep -Seconds 1
python -u tests/run_tests.py
