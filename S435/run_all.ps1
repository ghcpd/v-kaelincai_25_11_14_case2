# PowerShell equivalent to run_all.sh
Set-StrictMode -Version Latest
Push-Location Project_A_BaselineUI
.\run_tests.ps1
Pop-Location
Push-Location Project_B_ImprovedUI
.\run_tests.ps1
Pop-Location
python .\scripts\generate_report.py
Write-Host "All tests complete. See results/compare_report.md"