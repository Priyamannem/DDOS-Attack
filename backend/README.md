# DDoS Attack Prevention and Monitoring System

## 🛡️ Overview

A production-ready **DDoS Prevention System** built with FastAPI and PostgreSQL. This system provides:

- **Real-time Rate Limiting** (per-second and per-minute)
- **Anomaly Detection** with multiple pattern recognition
- **IP Reputation Management** (blacklist/whitelist)
- **Automatic Threat Mitigation**
- **Comprehensive Logging** and Analytics
- **Admin Control Panel** via REST API
- **Traffic Simulation** for testing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Request                        │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              DDoS Protection Middleware                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  1. IP Extraction & Reputation Check            │   │
│  │  2. Blacklist/Whitelist Verification            │   │
│  │  3. Rate Limiting (Sliding Window)              │   │
│  │  4. Anomaly Detection (Multi-Pattern)           │   │
│  │  5. Auto-Blocking & Logging                     │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       ↓
         ┌─────────────┴──────────────┐
         │                             │
    ALLOWED                        BLOCKED
         │                             │
         ↓                             ↓
  ┌─────────────┐              ┌──────────────┐
  │  Process    │              │  Return 429  │
  │  Request    │              │  + Metadata  │
  └─────────────┘              └──────────────┘
         │
         ↓
  ┌─────────────────────────────────────┐
  │      PostgreSQL Database             │
  │  ├─ ip_activity                      │
  │  ├─ logs                             │
  │  ├─ rules                            │
  │  ├─ blacklist                        │
  │  ├─ whitelist                        │
  │  └─ traffic_stats                    │
  └─────────────────────────────────────┘
```

---

## 📋 Prerequisites

- **Python**: 3.10+
- **PostgreSQL**: 14+
- **System**: Windows/Linux/macOS

---

## 🚀 Quick Start

### 1. Database Setup

```powershell
# Install PostgreSQL (if not already installed)
# Download from: https://www.postgresql.org/download/

# Create database
psql -U postgres
CREATE DATABASE ddos_db;
\q
```

### 2. Backend Setup

```powershell
# Navigate to backend directory
cd C:\Desktop\projects\DDOS_1\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file with your database credentials
notepad .env
```

### 3. Update `.env` File

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ddos_db
```

### 4. Run the Application

```powershell
# Start the server
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📡 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | API information |
| GET | `/protected-resource` | Example protected endpoint |
| POST | `/test-endpoint` | Test POST endpoint |

### Admin Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/rules` | Get current protection rules |
| POST | `/admin/update_rules` | Update protection rules |
| GET | `/admin/logs/recent` | Get recent log entries |
| GET | `/admin/traffic/stats` | Get traffic statistics |
| GET | `/admin/ip/{ip}` | Get IP activity details |
| POST | `/admin/add_to_blacklist` | Add IP to blacklist |
| POST | `/admin/add_to_whitelist` | Add IP to whitelist |
| POST | `/admin/remove_ip` | Remove IP from lists |
| POST | `/admin/unblock_ip` | Unblock temporarily blocked IP |
| GET | `/admin/blocked_ips` | Get all blocked IPs |
| GET | `/admin/blacklist` | Get blacklist |
| GET | `/admin/whitelist` | Get whitelist |

### Simulation Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/simulate/high-traffic` | Simulate high traffic |
| GET | `/simulate/ddos-attack` | Simulate DDoS attack |

---

## 🧪 Testing

### Using Traffic Simulator

```powershell
# Run interactive simulator
python tests/traffic_simulator.py
```

**Available Tests:**
1. Normal Traffic Simulation
2. Rate Limit Attack
3. Distributed DDoS Attack
4. IP Reputation Testing
5. View Statistics

### Using API Directly

```powershell
# Test rate limiting
for ($i=0; $i -lt 100; $i++) {
    Invoke-RestMethod -Uri http://localhost:8000/protected-resource
}

# Simulate high traffic
Invoke-RestMethod -Uri "http://localhost:8000/simulate/high-traffic?count=1000&ip=auto"

# View logs
Invoke-RestMethod -Uri http://localhost:8000/admin/logs/recent
```

---

## ⚙️ Configuration

### Default Rate Limits

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_req_per_sec` | 10 | Max requests per second |
| `max_req_per_min` | 100 | Max requests per minute |
| `block_duration` | 300 | Block duration in seconds |
| `anomaly_threshold` | 5000 | Global requests/min threshold |

### Updating Rules

```bash
curl -X POST http://localhost:8000/admin/update_rules \
  -H "Content-Type: application/json" \
  -d '{
    "max_req_per_sec": 20,
    "max_req_per_min": 200,
    "block_duration": 600,
    "anomaly_threshold": 10000
  }'
```

---

## 🔐 Security Features

### 1. Rate Limiting
- **Sliding window** counters
- Per-second AND per-minute enforcement
- Automatic blocking on violation

### 2. Anomaly Detection
- Global traffic spike detection
- Repeated endpoint access
- High request velocity
- Burst pattern detection
- **Auto-blocking** on multiple anomalies

### 3. IP Reputation
- **Blacklist**: Permanent blocks
- **Whitelist**: Bypass all checks
- Dynamic blocking with TTL

### 4. Comprehensive Logging
- Every request logged to database
- Status tracking (allowed/blocked/suspicious)
- Reason tracking for analytics

---

## 📊 Database Schema

### Tables

1. **ip_activity**: IP tracking and counters
2. **logs**: Request logs
3. **rules**: Protection rules (versioned)
4. **blacklist**: Permanently blocked IPs
5. **whitelist**: Trusted IPs
6. **traffic_stats**: Aggregated statistics

---

## 🛠️ Development

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── logger.py        # Logging setup
│   │   └── utils.py         # Utilities
│   ├── models/              # SQLModel database models
│   │   ├── ip_activity.py
│   │   ├── logs.py
│   │   ├── rules.py
│   │   ├── blacklist.py
│   │   ├── whitelist.py
│   │   └── traffic_stats.py
│   ├── middleware/          # Security middleware
│   │   ├── rate_limiter.py
│   │   ├── anomaly_detector.py
│   │   ├── ip_reputation.py
│   │   └── mitigation.py
│   ├── routers/             # API routes
│   │   ├── admin.py
│   │   ├── simulate.py
│   │   └── public.py
│   └── services/            # Business logic
│       ├── ip_service.py
│       ├── logs_service.py
│       ├── rules_service.py
│       ├── stats_service.py
│       └── traffic_service.py
├── tests/
│   └── traffic_simulator.py
├── logs/
├── requirements.txt
└── .env
```

---

## 📈 Monitoring

### View Real-Time Stats

```bash
# Get current rules
curl http://localhost:8000/admin/rules

# Get traffic stats
curl http://localhost:8000/admin/traffic/stats

# Get recent logs
curl http://localhost:8000/admin/logs/recent?limit=50

# Check specific IP
curl http://localhost:8000/admin/ip/192.168.1.100
```

### Log Files

Logs are written to:
- **Console**: Real-time colored output
- **File**: `logs/traffic.log` (JSON format)

---

## 🚨 Troubleshooting

### Database Connection Error

```
Check your .env DATABASE_URL
Ensure PostgreSQL is running
Verify credentials
```

### Permission Denied on Port 8000

```powershell
# Run on different port
uvicorn app.main:app --port 8080
```

### Rate Limiting Not Working

```
Check database connection
Verify rules are configured
Check IP extraction (proxies may affect this)
```

---

## 🔄 Reset System

```python
# In Python shell
from app.database import engine
from sqlmodel import SQLModel

# Drop all tables
SQLModel.metadata.drop_all(engine)

# Recreate tables
SQLModel.metadata.create_all(engine)
```

---

## 📝 License

MIT License - Feel free to use for cybersecurity education and production.

---

## 👨‍💻 Support

For issues or feature requests, check the API documentation at `/docs`.

---

## 🎯 Next Steps

Once backend is verified:
1. **Frontend**: React dashboard with real-time monitoring
2. **Deployment**: Docker containerization
3. **Advanced Features**: Machine learning-based detection

---

**Built with FastAPI + PostgreSQL + SQLModel**
