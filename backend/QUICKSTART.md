# DDoS Prevention System - Quick Setup Guide

## 🚀 5-Minute Setup

### Prerequisites
- ✅ Python 3.10+
- ✅ PostgreSQL 14+
- ✅ PowerShell (Windows) or Bash (Linux/Mac)

---

## Step-by-Step Setup

### 1️⃣ Install PostgreSQL

**Windows:**
```powershell
# Download from: https://www.postgresql.org/download/windows/
# Run installer and remember your password
```

**Create Database:**
```powershell
# Open PowerShell and run:
psql -U postgres
# Enter your password, then:
CREATE DATABASE ddos_db;
\q
```

---

### 2️⃣ Backend Setup (Automated)

```powershell
# Navigate to backend directory
cd C:\Desktop\projects\DDOS_1\backend

# Run setup script (does everything for you!)
.\setup.ps1
```

**What the script does:**
- ✅ Creates virtual environment
- ✅ Installs dependencies
- ✅ Sets up .env file

---

### 3️⃣ Configure Database Connection

```powershell
# Open .env file
notepad .env

# Update this line with your PostgreSQL password:
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/ddos_db
```

---

### 4️⃣ Initialize Database

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Initialize database tables
python init_db.py
```

**You should see:**
```
✓ Database tables created
✓ Default rules created
✓ Added localhost to whitelist
✅ Database initialization completed successfully!
```

---

### 5️⃣ Start the Server

```powershell
# Option 1: Use start script
.\start_server.ps1

# Option 2: Manual start
python -m app.main
```

**Server will start on:** `http://localhost:8000`

---

## ✅ Verify Installation

### Test 1: Health Check
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

**Expected output:**
```json
{
  "status": "healthy",
  "service": "DDoS Prevention System",
  "timestamp": "..."
}
```

### Test 2: API Documentation
Open browser: `http://localhost:8000/docs`

You should see **Swagger UI** with all endpoints!

### Test 3: Protected Endpoint
```powershell
# Send a single request (should work)
Invoke-RestMethod -Uri http://localhost:8000/protected-resource

# Send 100 rapid requests (should get blocked)
1..100 | ForEach-Object { 
    Invoke-RestMethod -Uri http://localhost:8000/protected-resource 
}
```

---

## 🧪 Run Traffic Simulator

```powershell
# Start interactive simulator
python tests/traffic_simulator.py

# Select option:
# 1 = Normal traffic
# 2 = Rate limit attack (tests blocking)
# 3 = Distributed DDoS (tests anomaly detection)
```

---

## 📊 View System Stats

```powershell
# Get current rules
Invoke-RestMethod -Uri http://localhost:8000/admin/rules

# View recent logs
Invoke-RestMethod -Uri http://localhost:8000/admin/logs/recent

# Check blocked IPs
Invoke-RestMethod -Uri http://localhost:8000/admin/blocked_ips
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied on port 8000"
```powershell
# Run on different port
uvicorn app.main:app --port 8080
```

### Issue: "Database connection failed"
```
1. Check PostgreSQL is running
2. Verify .env DATABASE_URL
3. Test connection: psql -U postgres -d ddos_db
```

### Issue: "Module not found"
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Virtual environment not activated"
```powershell
# Activate it
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

---

## 🎯 Testing DDoS Protection

### Test Rate Limiting
```powershell
# This will trigger rate limiting after 10 requests/second
$uri = "http://localhost:8000/protected-resource"
1..100 | ForEach-Object { 
    try {
        Invoke-RestMethod -Uri $uri
        Write-Host "Request $_: OK" -ForegroundColor Green
    } catch {
        Write-Host "Request $_: BLOCKED" -ForegroundColor Red
    }
}
```

### Test IP Blocking
```powershell
# Add IP to blacklist
$body = @{
    ip = "1.2.3.4"
    reason = "test"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/admin/add_to_blacklist `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Verify blacklist
Invoke-RestMethod -Uri http://localhost:8000/admin/blacklist
```

---

## 📝 Next Steps

Once backend is working:

1. ✅ **Test all endpoints** via Swagger UI
2. ✅ **Run traffic simulator** to verify protection
3. ✅ **Review logs** to understand system behavior
4. ⏳ **Wait for frontend** development (React dashboard)
5. ⏳ **Database setup** (we'll do this together)

---

## 🆘 Need Help?

If something isn't working:
1. Check server logs in console
2. Review `logs/traffic.log` file
3. Verify PostgreSQL is running: `Get-Service postgresql*`
4. Test database connection: `psql -U postgres -d ddos_db`

---

**Ready to proceed?** Let me know when the backend is running smoothly! 🚀
