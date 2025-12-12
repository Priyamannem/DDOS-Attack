# Backend Setup & Verification Checklist

Use this checklist to ensure your DDoS Prevention System backend is properly configured and working.

---

## ✅ Pre-Installation Checklist

### System Requirements
- [ ] Python 3.10 or higher installed
  ```powershell
  python --version
  # Should show: Python 3.10.x or higher
  ```

- [ ] PostgreSQL 14+ installed
  ```powershell
  psql --version
  # Should show: psql (PostgreSQL) 14.x or higher
  ```

- [ ] PowerShell available (Windows)
  ```powershell
  $PSVersionTable.PSVersion
  # Should work without error
  ```

---

## 📦 Installation Steps

### Step 1: Database Setup
- [ ] PostgreSQL service is running
  ```powershell
  Get-Service postgresql*
  # Status should be "Running"
  ```

- [ ] Database 'ddos_db' created
  ```powershell
  psql -U postgres -c "SELECT 1"
  # Then run: CREATE DATABASE ddos_db;
  ```

### Step 2: Backend Setup
- [ ] Navigate to backend directory
  ```powershell
  cd C:\Desktop\projects\DDOS_1\backend
  ```

- [ ] Run setup script
  ```powershell
  .\setup.ps1
  ```
  
  **Expected output:**
  - ✓ Python found
  - ✓ Virtual environment created
  - ✓ Virtual environment activated
  - ✓ Dependencies installed successfully
  - ✓ .env file created

### Step 3: Configuration
- [ ] Edit .env file with your PostgreSQL password
  ```powershell
  notepad .env
  ```
  
  **Update this line:**
  ```
  DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ddos_db
  ```

- [ ] Save and close .env file

### Step 4: Database Initialization
- [ ] Activate virtual environment (if not already active)
  ```powershell
  .\venv\Scripts\activate
  # You should see (venv) in your prompt
  ```

- [ ] Initialize database
  ```powershell
  python init_db.py
  ```
  
  **Expected output:**
  ```
  Initializing database...
  ✓ Database tables created
  ✓ Default rules created
  ✓ Added localhost to whitelist
  ✓ Added example blacklist entry
  ✅ Database initialization completed successfully!
  ```

---

## 🚀 Starting the Server

### Option 1: Use Start Script (Recommended)
- [ ] Run start script
  ```powershell
  .\start_server.ps1
  ```

### Option 2: Manual Start
- [ ] Activate virtual environment
  ```powershell
  .\venv\Scripts\activate
  ```

- [ ] Start server
  ```powershell
  python -m app.main
  ```

**Expected startup logs:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Starting DDoS Prevention System...
INFO:     Creating database tables...
INFO:     Database initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Verification Tests

### Test 1: Health Check
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "DDoS Prevention System",
  "timestamp": "2024-XX-XX..."
}
```
- [ ] Health check returns 200 OK
- [ ] Response is valid JSON

### Test 2: API Documentation
- [ ] Open browser to http://localhost:8000/docs
- [ ] Swagger UI loads successfully
- [ ] All endpoints are visible:
  - [ ] Admin endpoints (14 routes)
  - [ ] Simulation endpoints (2 routes)
  - [ ] Public endpoints (4 routes)

### Test 3: Database Connection
```powershell
Invoke-RestMethod -Uri http://localhost:8000/admin/rules
```

**Expected response:**
```json
{
  "success": true,
  "rules": {
    "id": 1,
    "max_req_per_sec": 10,
    "max_req_per_min": 100,
    "block_duration": 300,
    "anomaly_threshold": 5000,
    "updated_at": "..."
  }
}
```
- [ ] Rules endpoint returns data
- [ ] Default rules are present

### Test 4: Rate Limiting
```powershell
# Send 20 rapid requests
1..20 | ForEach-Object {
    try {
        Invoke-RestMethod -Uri http://localhost:8000/protected-resource
        Write-Host "Request $_: OK" -ForegroundColor Green
    } catch {
        Write-Host "Request $_: BLOCKED" -ForegroundColor Red
    }
}
```

**Expected behavior:**
- [ ] First ~10 requests succeed (200 OK)
- [ ] Subsequent requests get blocked (429 Too Many Requests)
- [ ] Block response includes retry_after field

### Test 5: Logging
```powershell
Invoke-RestMethod -Uri http://localhost:8000/admin/logs/recent
```

**Expected response:**
```json
{
  "success": true,
  "count": X,
  "logs": [...]
}
```
- [ ] Logs endpoint returns data
- [ ] Recent requests appear in logs
- [ ] Log entries have: ip, endpoint, status, reason

### Test 6: IP Reputation
```powershell
# Add to blacklist
$body = @{ ip = "1.2.3.4"; reason = "test" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/admin/add_to_blacklist -Method POST -Body $body -ContentType "application/json"

# Verify blacklist
Invoke-RestMethod -Uri http://localhost:8000/admin/blacklist
```

**Expected behavior:**
- [ ] Add to blacklist succeeds
- [ ] IP appears in blacklist
- [ ] Blacklist count increases

### Test 7: Traffic Simulation
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/simulate/high-traffic?count=100&ip=auto"
```

**Expected response:**
```json
{
  "success": true,
  "message": "Simulated 100 requests",
  "mode": "auto",
  ...
}
```
- [ ] Simulation completes without errors
- [ ] Response includes request count
- [ ] Database shows increased activity

### Test 8: Interactive Simulator
```powershell
python tests/traffic_simulator.py
```

**Test all options:**
- [ ] Option 1: Normal Traffic - runs without errors
- [ ] Option 2: Rate Limit Attack - shows blocking
- [ ] Option 3: Distributed DDoS - shows blocking
- [ ] Option 4: IP Reputation - blacklist works
- [ ] Option 5: View Statistics - returns data

---

## 📊 Performance Checks

### Database
- [ ] PostgreSQL service is running
  ```powershell
  Get-Service postgresql*
  ```

- [ ] Database contains tables
  ```powershell
  psql -U postgres -d ddos_db -c "\dt"
  # Should show: ip_activity, logs, rules, blacklist, whitelist, traffic_stats
  ```

- [ ] Table counts are reasonable
  ```powershell
  psql -U postgres -d ddos_db -c "SELECT COUNT(*) FROM logs;"
  ```

### Log Files
- [ ] Log directory exists
  ```powershell
  Test-Path "logs"
  # Should return: True
  ```

- [ ] Log file is being written
  ```powershell
  Get-Content logs/traffic.log -Tail 10
  # Should show recent JSON log entries
  ```

---

## 🐛 Troubleshooting

### Issue: "Port 8000 already in use"
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or run on different port
uvicorn app.main:app --port 8080
```
- [ ] Port issue resolved

### Issue: "Database connection failed"
```powershell
# Test PostgreSQL connection
psql -U postgres -d ddos_db -c "SELECT 1;"

# If fails, check:
# 1. PostgreSQL is running
# 2. .env DATABASE_URL is correct
# 3. Password is correct
```
- [ ] Database connection works

### Issue: "Module not found"
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```
- [ ] All imports work

### Issue: "Permission denied"
```powershell
# Run PowerShell as Administrator
# Or change execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
- [ ] Scripts run without permission errors

---

## 📝 Final Checklist

### Core Functionality
- [ ] Server starts without errors
- [ ] Health endpoint works
- [ ] API documentation accessible
- [ ] Database connection successful
- [ ] All tables created

### Security Features
- [ ] Rate limiting blocks excessive requests
- [ ] Anomaly detection logs suspicious activity
- [ ] Blacklist blocks IPs
- [ ] Whitelist bypasses checks
- [ ] Logs are created for all requests

### Admin Features
- [ ] Can view current rules
- [ ] Can update rules
- [ ] Can view logs
- [ ] Can view statistics
- [ ] Can manage IP reputation

### Testing
- [ ] Traffic simulator works
- [ ] All simulation modes run
- [ ] Statistics update correctly
- [ ] Logs are queryable

---

## 🎯 Ready for Production?

If all checks above are ✅, your backend is **production-ready**!

### Next Steps:
1. ✅ Backend complete and verified
2. ⏳ **Frontend development** (React dashboard)
3. ⏳ **Database optimization** (performance tuning)
4. ⏳ **Deployment** (Docker, cloud hosting)

---

## 📞 Need Help?

If any check fails:
1. Review error messages carefully
2. Check logs: `Get-Content logs/traffic.log -Tail 50`
3. Verify PostgreSQL: `Get-Service postgresql*`
4. Test database: `psql -U postgres -d ddos_db`
5. Check .env configuration

---

**Once all checks pass, you're ready to move forward! 🚀**
