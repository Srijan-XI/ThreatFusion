# 🚀 ThreatFusion Web Interface - Startup Scripts

Easy one-click startup scripts for both Windows and Linux/Mac!

---

## 📋 **Available Scripts**

### Windows: `run.bat`
Batch script for Windows systems

### Linux/Mac: `run.sh`
Bash script for Unix-based systems

---

## 🎯 **Quick Start**

### Windows:
```batch
cd web
run.bat
```
**or**
- Double-click `run.bat` in File Explorer

### Linux/Mac:
```bash
cd web
chmod +x run.sh  # First time only
./run.sh
```

---

## ✨ **What the Scripts Do**

### 1. **Environment Check**
- ✅ Verifies Node.js is installed
- ✅ Verifies Python is installed
- ✅ Checks for npm and pip

### 2. **Dependency Installation**
- ✅ Installs npm packages (if needed)
- ✅ Creates Python virtual environment (if needed)
- ✅ Installs Python packages (if needed)

### 3. **Service Startup**
- ✅ Starts FastAPI backend on port 8000
- ✅ Starts React frontend on port 3000
- ✅ Opens browser automatically

### 4. **Error Handling**
- ✅ Checks for installation errors
- ✅ Validates service startup
- ✅ Provides helpful error messages
- ✅ Logs output for debugging

---

## 🖥️ **Windows Script (`run.bat`)**

### Features:
- ✅ Colored console output
- ✅ Progress indicators
- ✅ Opens services in new console windows
- ✅ Auto-opens browser after 3 seconds
- ✅ Keeps windows open for monitoring

### Usage:
```batch
# Option 1: Double-click
run.bat

# Option 2: Command line
cd p:\CODE-X\ThreatFusion\web
.\run.bat
```

### What You'll See:
```
========================================
  ThreatFusion Web Interface
  Startup Script for Windows
========================================

[*] Installing dependencies...
[1/2] Starting FastAPI Backend...
      URL: http://localhost:8000
      Docs: http://localhost:8000/docs

[2/2] Starting React Frontend...
      URL: http://localhost:3000

========================================
  Services Started Successfully!
========================================

Frontend: http://localhost:3000
Backend:  http://localhost:8000
API Docs: http://localhost:8000/docs
```

### Services Run In:
- **Backend**: Separate console window (green header)
- **Frontend**: Separate console window (green header)

### To Stop Services:
- Close the console windows
- Or press `Ctrl+C` in each window

---

## 🐧 **Linux/Mac Script (`run.sh`)**

### Features:
- ✅ Colored terminal output
- ✅ Progress indicators
- ✅ Services run in background
- ✅ Auto-opens browser
- ✅ Graceful shutdown with Ctrl+C
- ✅ Process ID tracking
- ✅ Log file generation

### First-Time Setup:
```bash
# Make script executable
chmod +x run.sh
```

### Usage:
```bash
cd /path/to/ThreatFusion/web
./run.sh
```

### What You'll See:
```
========================================
  ThreatFusion Web Interface
  Startup Script for Linux/Mac
========================================

[*] Installing dependencies...
[1/2] Starting FastAPI Backend...
      URL: http://localhost:8000
      Docs: http://localhost:8000/docs

[2/2] Starting React Frontend...
      URL: http://localhost:3000

========================================
  Services Started Successfully!
========================================

Frontend: http://localhost:3000
Backend:  http://localhost:8000
API Docs: http://localhost:8000/docs

Backend PID:  12345
Frontend PID: 12346

Press Ctrl+C to stop all services.

Logs are available at:
  Backend:  /tmp/threatfusion-backend.log
  Frontend: /tmp/threatfusion-frontend.log
```

### Services Run:
- **Backend**: Background process (logs to `/tmp/threatfusion-backend.log`)
- **Frontend**: Background process (logs to `/tmp/threatfusion-frontend.log`)

### To Stop Services:
- Press `Ctrl+C` in the terminal
- Script will automatically cleanup both processes

### View Logs:
```bash
# Backend logs
tail -f /tmp/threatfusion-backend.log

# Frontend logs
tail -f /tmp/threatfusion-frontend.log
```

---

## 🔧 **Prerequisites**

### Required Software:

#### Windows:
- ✅ **Node.js** 18+ - https://nodejs.org/
- ✅ **Python** 3.8+ - https://python.org/
- ✅ **npm** (included with Node.js)
- ✅ **pip** (included with Python)

#### Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm python3 python3-pip python3-venv

# Fedora/RHEL
sudo dnf install nodejs npm python3 python3-pip

# Arch
sudo pacman -S nodejs npm python python-pip
```

#### Mac:
```bash
# Using Homebrew
brew install node python3

# Or download from:
# Node.js: https://nodejs.org/
# Python: https://python.org/
```

---

## 📊 **Access URLs**

After running the scripts, access:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Web Interface Dashboard |
| **Backend** | http://localhost:8000 | FastAPI Server |
| **API Docs** | http://localhost:8000/docs | Swagger UI Documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API Docs |

---

## ❌ **Troubleshooting**

### "Node.js is not installed"
**Solution:** Install Node.js from https://nodejs.org/

### "Python is not installed"
**Solution:** Install Python from https://python.org/

### "Port already in use"
**Solution:** 
- Stop other services using port 3000 or 8000
- Or modify ports in configuration files

### "Permission denied" (Linux/Mac)
**Solution:**
```bash
chmod +x run.sh
```

### "Dependencies failed to install"
**Solution:**
```bash
# Clear cache and reinstall
cd web
rm -rf node_modules
npm install

# For Python
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
```

### Services Won't Start
**Check logs:**
- Windows: Look at console window output
- Linux/Mac: Check `/tmp/threatfusion-*.log`

---

## 🎨 **Script Features Summary**

| Feature | Windows (`run.bat`) | Linux/Mac (`run.sh`) |
|---------|-------------------|---------------------|
| Colored Output | ✅ | ✅ |
| Dependency Check | ✅ | ✅ |
| Auto-Install | ✅ | ✅ |
| Service Startup | ✅ | ✅ |
| Auto Browser Open | ✅ | ✅ |
| Process Tracking | ⚠️ Separate Windows | ✅ PIDs Shown |
| Log Files | ❌ | ✅ |
| Graceful Shutdown | ⚠️ Close Windows | ✅ Ctrl+C |
| Error Messages | ✅ | ✅ |

---

## 🎯 **Comparison with Other Methods**

### Option 1: Startup Scripts (EASIEST! ⭐)
```bash
./run.sh  # or run.bat
```
**Pros:**
- ✅ One command does everything
- ✅ Auto-checks dependencies
- ✅ Auto-installs if needed
- ✅ Opens browser automatically
- ✅ Colored output
- ✅ Error handling

### Option 2: PowerShell Script
```powershell
.\start-all.ps1
```
**Pros:**
- ✅ Windows PowerShell specific
- ✅ Opens new windows

### Option 3: Manual Startup
```bash
# Terminal 1
cd web/api
uvicorn main:app --reload --port 8000

# Terminal 2
cd web
npm run dev
```
**Pros:**
- ✅ Full control
**Cons:**
- ❌ Need 2 terminals
- ❌ Manual dependency checks
- ❌ More steps

---

## 🚀 **Recommended Usage**

### For Development:
Use the startup scripts for quick testing:
```bash
./run.sh  # or run.bat
```

### For Production:
Use process managers:
- **Windows**: NSSM (Non-Sucking Service Manager)
- **Linux**: systemd, supervisor, or PM2

---

## 📝 **Notes**

- Scripts automatically create Python virtual environment
- Scripts automatically install dependencies
- Backend runs with auto-reload (development mode)
- Frontend runs with Vite dev server
- Changes to code will auto-reload services

---

## ✅ **Quick Reference**

### Windows (CMD):
```batch
cd web
run.bat
```

### Windows (PowerShell):
```powershell
cd web
.\run.bat
```

### Linux/Mac:
```bash
cd web
./run.sh
```

---

**Made with ❤️ for ThreatFusion**
