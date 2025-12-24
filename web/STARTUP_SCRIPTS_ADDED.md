#  Startup Scripts!

### 1. **`run.bat`** - Windows Startup Script
**Location:** `web/run.bat`

**Features:**
- ✅ Colored console output
- ✅ Automatic dependency checking
- ✅ Auto-install npm packages
- ✅ Auto-create Python virtual environment
- ✅ Auto-install Python packages
- ✅ Starts backend in new window
- ✅ Starts frontend in new window
- ✅ Opens browser automatically
- ✅ Comprehensive error messages

**Usage:**
```batch
cd web
run.bat
```
Or simply **double-click** `run.bat` in File Explorer!

---

### 2. **`run.sh`** - Linux/Mac Startup Script
**Location:** `web/run.sh`

**Features:**
- ✅ Colored terminal output
- ✅ Automatic dependency checking
- ✅ Auto-install npm packages
- ✅ Auto-create Python virtual environment
- ✅ Auto-install Python packages
- ✅ Runs services in background
- ✅ Process ID tracking
- ✅ Log file generation
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Opens browser automatically
- ✅ Comprehensive error messages

**First-Time Setup:**
```bash
cd web
chmod +x run.sh
```

**Usage:**
```bash
cd web
./run.sh
```

**Logs location:**
- Backend: `/tmp/threatfusion-backend.log`
- Frontend: `/tmp/threatfusion-frontend.log`

---

### 3. **`RUN_SCRIPTS_GUIDE.md`** - Complete Documentation
**Location:** `web/RUN_SCRIPTS_GUIDE.md`

Complete guide covering:
- ✅ How to use both scripts
- ✅ Prerequisites
- ✅ Troubleshooting
- ✅ Comparison with other methods
- ✅ Feature summaries

---

## 🚀 **How to Start the Web Interface Now**

### Option 1: Startup Scripts (EASIEST! ⭐)

**Windows:**
```batch
cd p:\CODE-X\ThreatFusion\web
run.bat
```

**Linux/Mac:**
```bash
cd /path/to/ThreatFusion/web
chmod +x run.sh  # First time only
./run.sh
```

### Option 2: PowerShell Script
```powershell
cd p:\CODE-X\ThreatFusion\web
.\start-all.ps1
```

### Option 3: Manual (2 terminals)
```bash
# Terminal 1 - Backend
cd web/api
../.venv/Scripts/activate  # Windows
# or
source ../.venv/bin/activate  # Linux/Mac
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd web
npm run dev
```

---

## 📊 **What the Scripts Do**

```
┌─────────────────────────────────────┐
│  1. Check Node.js & Python          │
│     ✓ Installed? Continue           │
│     ✗ Missing? Show error & exit    │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  2. Check Dependencies               │
│     • node_modules/ exists?          │
│       No → npm install               │
│     • .venv/ exists?                 │
│       No → python -m venv .venv      │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  3. Install Python Packages          │
│     pip install -r requirements.txt  │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  4. Start Backend (Port 8000)        │
│     uvicorn main:app --reload        │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  5. Start Frontend (Port 3000)       │
│     npm run dev                      │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  6. Open Browser                     │
│     http://localhost:3000            │
└─────────────────────────────────────┘
            ↓
        SUCCESS! 🎉
```

---

## ✨ **Script Features**

| Feature | `run.bat` (Windows) | `run.sh` (Linux/Mac) |
|---------|-------------------|---------------------|
| **Auto Dependency Check** | ✅ | ✅ |
| **Auto Install** | ✅ | ✅ |
| **Colored Output** | ✅ | ✅ |
| **Error Messages** | ✅ | ✅ |
| **Service Startup** | ✅ New Windows | ✅ Background |
| **Browser Auto-Open** | ✅ | ✅ |
| **Process Tracking** | ⚠️ Separate | ✅ PIDs |
| **Log Files** | ❌ | ✅ |
| **Graceful Shutdown** | Close Windows | ✅ Ctrl+C |

---

## 🎯 **Quick Start Guide**

### For Windows Users:

1. **Navigate to web folder:**
   ```batch
   cd p:\CODE-X\ThreatFusion\web
   ```

2. **Run the script:**
   ```batch
   run.bat
   ```
   Or **double-click** `run.bat` in File Explorer!

3. **Wait for browser to open** (automatic)

4. **Services will open in new windows:**
   - ThreatFusion API Backend
   - ThreatFusion Web Frontend

5. **Access the interface:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### For Linux/Mac Users:

1. **Navigate to web folder:**
   ```bash
   cd /path/to/ThreatFusion/web
   ```

2. **Make script executable (first time only):**
   ```bash
   chmod +x run.sh
   ```

3. **Run the script:**
   ```bash
   ./run.sh
   ```

4. **Wait for browser to open** (automatic)

5. **Services run in background:**
   - View PIDs in terminal output
   - Check logs: `/tmp/threatfusion-*.log`

6. **Stop services:**
   - Press `Ctrl+C` in terminal
   - Script will cleanup automatically

---

## 📝 **Example Output**

### Windows (`run.bat`):
```
========================================
  ThreatFusion Web Interface
  Startup Script for Windows
========================================

[*] Installing npm dependencies... DONE
[*] Installing Python dependencies... DONE

========================================
  Starting Services
========================================

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

Both services are running in separate windows.
Close those windows to stop the services.

Opening browser in 3 seconds...
```

### Linux/Mac (`run.sh`):
```
========================================
  ThreatFusion Web Interface
  Startup Script for Linux/Mac
========================================

[*] Installing npm dependencies... DONE
[*] Installing Python dependencies... DONE

========================================
  Starting Services
========================================

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

Waiting for services... (Ctrl+C to stop)
```

---

## 🎊 **All Startup Methods**

You now have **4 different ways** to start the web interface:

### 1. **`run.bat`** (Windows - Easiest!)
```batch
cd web
run.bat
```

### 2. **`run.sh`** (Linux/Mac - Easiest!)
```bash
cd web
./run.sh
```

### 3. **`start-all.ps1`** (PowerShell)
```powershell
cd web
.\start-all.ps1
```

### 4. **Manual** (Advanced)
```bash
# Terminal 1
cd web/api
uvicorn main:app --reload --port 8000

# Terminal 2
cd web
npm run dev
```

---

## 📚 **Documentation Files**

All startup documentation is now available:

1. **`run.bat`** - Windows startup script
2. **`run.sh`** - Linux/Mac startup script
3. **`start-all.ps1`** - PowerShell startup script
4. **`RUN_SCRIPTS_GUIDE.md`** - Complete guide
5. **`QUICKSTART.md`** - Quick start instructions
6. **`README.md`** - Full documentation

---

## ✅ **Complete!**

You now have **easy one-click startup scripts** for:
- ✅ Windows (.bat)
- ✅ Linux (.sh)
- ✅ Mac (.sh)
- ✅ PowerShell (.ps1)

**Just run the script and you're ready to go! 🚀**

---

**Made with ❤️ for ThreatFusion**
