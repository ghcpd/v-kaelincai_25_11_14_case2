$RootDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Push-Location $RootDir\..\
./setup.sh
Pop-Location
Push-Location $RootDir
mkdir logs -ErrorAction SilentlyContinue
mkdir results -ErrorAction SilentlyContinue
mkdir screenshots -ErrorAction SilentlyContinue
pytest -q tests/test_post_visual.py 2>&1 | Tee-Object -FilePath logs\log_post.txt
pytest -q tests/test_post_css_assertions.py 2>&1 | Tee-Object -FilePath -Append logs\log_post.txt
pytest -q tests/test_post_a11y.py 2>&1 | Tee-Object -FilePath -Append logs\log_post.txt
Pop-Location
Write-Host "Project B tests complete. Results in results/ and screenshots/."
