# DDoS Prevention System - Setup and Run Script
# Run this script from PowerShell

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  DDoS PREVENTION SYSTEM - BACKEND SETUP" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Step 1: Check Python
Write-Host "`n[1/6] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Step 2: Create virtual environment
Write-Host "`n[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ⚠ Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 5: Setup environment file
Write-Host "`n[5/6] Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ⚠ .env file already exists" -ForegroundColor Yellow
} else {
    Copy-Item .env.example .env
    Write-Host "  ✓ .env file created from template" -ForegroundColor Green
    Write-Host "  ⚠ IMPORTANT: Edit .env file with your PostgreSQL credentials!" -ForegroundColor Yellow
}

# Step 6: Database check
Write-Host "`n[6/6] Database setup..." -ForegroundColor Yellow
Write-Host "  Before running the server, ensure:" -ForegroundColor Cyan
Write-Host "    1. PostgreSQL is installed and running" -ForegroundColor White
Write-Host "    2. Database 'ddos_db' is created" -ForegroundColor White
Write-Host "    3. .env file has correct DATABASE_URL" -ForegroundColor White

Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "  SETUP COMPLETED!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env file: notepad .env" -ForegroundColor White
Write-Host "  2. Initialize database: python init_db.py" -ForegroundColor White
Write-Host "  3. Start server: python -m app.main" -ForegroundColor White
Write-Host "  4. Access API docs: http://localhost:8000/docs" -ForegroundColor White

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
