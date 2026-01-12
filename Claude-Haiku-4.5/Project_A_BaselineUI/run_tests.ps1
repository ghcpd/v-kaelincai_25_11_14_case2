# PowerShell execution script for Project A - Baseline UI
Write-Host "=== Running Project A - Baseline UI Tests ===" -ForegroundColor Cyan

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python not found in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install requirements
if (Test-Path "requirements.txt") {
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    # Install playwright browsers
    Write-Host "Installing browser dependencies..." -ForegroundColor Yellow
    playwright install chromium
}

# Create necessary directories
Write-Host "Creating result directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "screenshots" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "results" | Out-Null

# Start logging
$logFile = "logs\log_pre.txt"
Write-Host "Starting baseline UI tests at $(Get-Date)" | Tee-Object $logFile

try {
    # Run visual tests
    Write-Host "Running visual tests..." -ForegroundColor Green | Tee-Object $logFile -Append
    Set-Location tests
    python test_pre_visual.py | Tee-Object ..\$logFile -Append

    # Run CSS assertion tests  
    Write-Host "Running CSS assertion tests..." -ForegroundColor Green | Tee-Object ..\$logFile -Append
    python test_pre_css_assertions.py | Tee-Object ..\$logFile -Append

    # Run accessibility tests
    Write-Host "Running accessibility tests..." -ForegroundColor Green | Tee-Object ..\$logFile -Append  
    python test_pre_a11y.py | Tee-Object ..\$logFile -Append

    Set-Location ..
    
    Write-Host "Baseline UI tests completed at $(Get-Date)" -ForegroundColor Cyan | Tee-Object $logFile -Append
    Write-Host "Results saved to:" -ForegroundColor Green
    Write-Host "  - screenshots/" -ForegroundColor White
    Write-Host "  - logs/log_pre.txt" -ForegroundColor White
    Write-Host "  - results/results_pre.json" -ForegroundColor White
    Write-Host "  - results/css_assertions_pre.json" -ForegroundColor White
    Write-Host "  - results/a11y_results_pre.json" -ForegroundColor White

} catch {
    Write-Host "Error running tests: $($_.Exception.Message)" -ForegroundColor Red | Tee-Object $logFile -Append
    exit 1
}