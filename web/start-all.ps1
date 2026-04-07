# Start ThreatFusion Web Interface

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ThreatFusion Web Interface Launcher  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$webPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if virtual environment exists
$venvPath = Join-Path $webPath "..\.venv"
$venvPath = [System.IO.Path]::GetFullPath($venvPath)
if (-Not (Test-Path $venvPath)) {
    Write-Host "[!] Virtual environment not found at: $venvPath" -ForegroundColor Yellow
    Write-Host "[*] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
}

# Function to start backend
function Start-Backend {
    Write-Host ""
    Write-Host "[1/2] Starting FastAPI Backend..." -ForegroundColor Green
    Write-Host "      URL: http://localhost:8000" -ForegroundColor Gray
    Write-Host "      Docs: http://localhost:8000/docs" -ForegroundColor Gray
    Write-Host ""
    
    $apiPath = Join-Path $webPath "api"
    Set-Location $apiPath
    
    # Activate virtual environment and start
    & "$venvPath\Scripts\Activate.ps1"
    pip install -r requirements.txt -q
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$venvPath\Scripts\Activate.ps1'; uvicorn main:app --reload --port 8000"
}

# Function to start frontend
function Start-Frontend {
    Write-Host ""
    Write-Host "[2/2] Starting React Frontend..." -ForegroundColor Green
    Write-Host "      URL: http://localhost:3000" -ForegroundColor Gray
    Write-Host ""
    
    Set-Location $webPath
    
    # Check if node_modules exists
    if (-Not (Test-Path "node_modules")) {
        Write-Host "[*] Installing npm dependencies..." -ForegroundColor Yellow
        npm install
    }
    
    Start-Sleep -Seconds 3
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$webPath'; npm run dev"
}

# Start both services
Start-Backend
Start-Frontend

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Services Started Successfully!       " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:  " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop services" -ForegroundColor Yellow
Write-Host ""

# Keep script running
Read-Host "Press Enter to exit"
