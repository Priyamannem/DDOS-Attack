# Start DDoS Prevention System Server
# Make sure you've run setup.ps1 first!

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "  Starting DDoS Prevention System..." -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "✗ Error: .env file not found!" -ForegroundColor Red
    Write-Host "  Run setup.ps1 first or copy .env.example to .env" -ForegroundColor Yellow
    exit 1
}

# Start server
Write-Host "`nStarting FastAPI server..." -ForegroundColor Yellow
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Health: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Gray

python -m app.main
