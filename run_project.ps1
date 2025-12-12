Write-Host "Starting DDOS Prevention Request..." -ForegroundColor Green

# Start Backend (API + Stats Aggregation)
Write-Host "Launching Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", ".\backend\start_server.ps1" -WorkingDirectory "backend"

# Start Continuous Traffic
Write-Host "Launching Traffic Generator..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "& {Set-Location 'backend'; .\myvenv\Scripts\python.exe continuous_traffic.py}" -WorkingDirectory "backend"

# Start Frontend
Write-Host "Launching Frontend..." -ForegroundColor Cyan
Set-Location "frontend"
npm run dev
