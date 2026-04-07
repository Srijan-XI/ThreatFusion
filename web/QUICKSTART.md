# ThreatFusion Web Interface - Startup Scripts

## Windows

### Start Everything (Recommended)
```powershell
.\start-all.ps1
```

### Start Backend Only
```powershell
cd web\api
..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

### Start Frontend Only
```powershell
cd web
npm run dev
```

## Access Points

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **WebSocket**: ws://localhost:8000/ws

## Quick Start

1. **First Time Setup:**
   ```powershell
   cd web
   npm install
   cd api
   pip install -r requirements.txt
   ```

2. **Start Services:**
   ```powershell
   # Terminal 1 - Backend
   cd web\api
   uvicorn main:app --reload --port 8000

   # Terminal 2 - Frontend
   cd web
   npm run dev
   ```

3. **Open Browser:**
   Navigate to http://localhost:3000

## Features

- Real-time threat monitoring
- Interactive dashboard with charts
- WebSocket live updates
- Scan management
- Threat analysis

Enjoy! 🚀
