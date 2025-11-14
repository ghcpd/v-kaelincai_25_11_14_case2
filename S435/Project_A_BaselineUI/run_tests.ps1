python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install
# Start server
$port=8001
Start-Process -NoNewWindow -FilePath python -ArgumentList "server/server_pre.py"
Start-Sleep -Seconds 1
python -u tests/run_tests.py
