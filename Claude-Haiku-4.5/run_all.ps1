# PowerShell master execution script - runs both projects and generates comparison report
Write-Host "=== UI/UX Improvement Evaluation - Full Test Suite ===" -ForegroundColor Cyan
Write-Host "Starting complete evaluation at $(Get-Date)" -ForegroundColor Yellow

# Clean up previous results
Write-Host "Cleaning up previous results..." -ForegroundColor Yellow
if (Test-Path "results") {
    Remove-Item "results\*" -Force -Recurse -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Force -Path "results" | Out-Null

# Run Project A - Baseline UI tests
Write-Host "" 
Write-Host "=== PHASE 1: Running Baseline UI Tests ===" -ForegroundColor Cyan
try {
    Set-Location "Project_A_BaselineUI"
    & ".\run_tests.ps1"
    Set-Location ".."
    
    # Copy baseline results to main results directory
    Write-Host "Copying baseline results..." -ForegroundColor Yellow
    if (Test-Path "Project_A_BaselineUI\screenshots\screenshot_pre_ui.png") {
        Copy-Item "Project_A_BaselineUI\screenshots\screenshot_pre_ui.png" "results\" -Force
    }
    if (Test-Path "Project_A_BaselineUI\results\*.json") {
        Copy-Item "Project_A_BaselineUI\results\*.json" "results\" -Force
    }
    if (Test-Path "Project_A_BaselineUI\logs\log_pre.txt") {
        Copy-Item "Project_A_BaselineUI\logs\log_pre.txt" "results\" -Force
    }
    
    Write-Host "Phase 1 completed successfully" -ForegroundColor Green
    
} catch {
    Write-Host "Error in Phase 1: $($_.Exception.Message)" -ForegroundColor Red
}

# Run Project B - Improved UI tests
Write-Host ""
Write-Host "=== PHASE 2: Running Improved UI Tests ===" -ForegroundColor Cyan
try {
    Set-Location "Project_B_ImprovedUI" 
    & ".\run_tests.ps1"
    Set-Location ".."
    
    # Copy improved results to main results directory
    Write-Host "Copying improved results..." -ForegroundColor Yellow
    if (Test-Path "Project_B_ImprovedUI\screenshots\screenshot_post_ui.png") {
        Copy-Item "Project_B_ImprovedUI\screenshots\screenshot_post_ui.png" "results\" -Force
    }
    if (Test-Path "Project_B_ImprovedUI\results\*.json") {
        Copy-Item "Project_B_ImprovedUI\results\*.json" "results\" -Force
    }
    if (Test-Path "Project_B_ImprovedUI\logs\log_post.txt") {
        Copy-Item "Project_B_ImprovedUI\logs\log_post.txt" "results\" -Force
    }
    
    Write-Host "Phase 2 completed successfully" -ForegroundColor Green
    
} catch {
    Write-Host "Error in Phase 2: $($_.Exception.Message)" -ForegroundColor Red
}

# Generate comparison report
Write-Host ""
Write-Host "=== PHASE 3: Generating Comparison Report ===" -ForegroundColor Cyan
try {
    python generate_comparison_report.py
    Write-Host "Phase 3 completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Error in Phase 3: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== EVALUATION COMPLETE ===" -ForegroundColor Cyan
Write-Host "Full evaluation completed at $(Get-Date)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Results available in:" -ForegroundColor Green
Write-Host "  - results\compare_report.md (Main comparison report)" -ForegroundColor White
Write-Host "  - results\screenshot_pre_ui.png (Baseline UI)" -ForegroundColor White  
Write-Host "  - results\screenshot_post_ui.png (Improved UI)" -ForegroundColor White
Write-Host "  - results\*.json (Detailed test results)" -ForegroundColor White
Write-Host "  - results\log_*.txt (Test execution logs)" -ForegroundColor White
Write-Host ""
Write-Host "To view the comparison report:" -ForegroundColor Green
Write-Host "  Get-Content results\compare_report.md" -ForegroundColor White