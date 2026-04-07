# ThreatFusion Web Interface

Practical startup and verification guide for the ThreatFusion web UI.

Last updated: April 2026

---

## Quick Access

1. Dashboard (Frontend)
   - http://localhost:3000
2. API Backend
   - http://localhost:8000
3. API Docs (Swagger)
   - http://localhost:8000/docs

---

## Current Stack

Frontend:
- React 18 + Vite
- Tailwind CSS
- Chart.js
- React Router

Backend:
- FastAPI
- Uvicorn
- WebSockets
- Pydantic

---

## Start the Web Interface

From the repository root:

### Option A (recommended)

```powershell
cd web
.\start-all.ps1
```

What this script does:
- Ensures the root `.venv` exists (creates if needed)
- Starts backend at port `8000`
- Starts frontend at port `3000`

### Option B (manual)

Terminal 1 (backend):

```powershell
cd web/api
..\..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Terminal 2 (frontend):

```powershell
cd web
npm install
npm run dev
```

---

## Health Checks

After startup, verify:

1. API responds:
   - Open http://localhost:8000
   - Expect JSON with `name`, `version`, and `status`

2. Frontend loads:
   - Open http://localhost:3000

3. Docs load:
   - Open http://localhost:8000/docs

4. UI-to-API path works:
   - Frontend uses Vite proxy for `/api` -> `http://localhost:8000`

---

## Core Features Available

- Real-time dashboard cards (scan/threat metrics)
- Active scan progress updates
- Threat distribution chart
- Recent threats list
- Component status indicators
- WebSocket updates for scan lifecycle events

---

## Troubleshooting (Windows)

1. Python virtual environment points to old Python path

Symptoms:
- Activation works, but Python commands fail or reference missing install path.

Fix:

```powershell
cd D:\CODE-X\ThreatFusion
Remove-Item -Recurse -Force .venv
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r web\api\requirements.txt
```

2. Frontend fails to start due to missing Node modules

```powershell
cd web
npm install
npm run dev
```

3. Port already in use (`3000` or `8000`)

- Stop existing process using that port.
- Then re-run startup.

---

## Related Docs

- `web/README.md`
- `web/QUICKSTART.md`
- `web/IMPLEMENTATION_SUMMARY.md`
- `web/GET_STARTED.md`

---

ThreatFusion Web v1.0.0
