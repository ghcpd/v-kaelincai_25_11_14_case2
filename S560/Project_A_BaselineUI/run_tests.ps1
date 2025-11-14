# Powershell equivalent runner
$RootDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Push-Location $RootDir\..\
./setup.sh
Pop-Location
Push-Location $RootDir
mkdir logs -ErrorAction SilentlyContinue
mkdir results -ErrorAction SilentlyContinue
mkdir screenshots -ErrorAction SilentlyContinue
pytest -q tests/test_pre_visual.py 2>&1 | Tee-Object -FilePath logs\log_pre.txt
pytest -q tests/test_pre_css_assertions.py 2>&1 | Tee-Object -FilePath -Append logs\log_pre.txt
pytest -q tests/test_pre_a11y.py 2>&1 | Tee-Object -FilePath -Append logs\log_pre.txt
Pop-Location
Write-Host "Project A tests complete. Results in results/ and screenshots/."
