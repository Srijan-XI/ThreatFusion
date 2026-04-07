#!/usr/bin/env python3
"""
ThreatFusion Web API
FastAPI backend for web interface integration
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import json
import os
import sys
from pathlib import Path
from enum import Enum

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Initialize FastAPI
app = FastAPI(
    title="ThreatFusion API",
    description="Unified Cybersecurity Analysis Platform API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead_connections = []
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        for connection in dead_connections:
            self.disconnect(connection)

manager = ConnectionManager()

# Data Models
class ScanStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ScanRequest(BaseModel):
    target_directory: Optional[str] = "data/samples"
    scan_type: str = "full"  # full, quick, custom
    enable_ml: bool = True
    enable_network: bool = True

class ScanResult(BaseModel):
    scan_id: str
    status: ScanStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    files_scanned: int = 0
    threats_detected: int = 0
    threat_summary: Dict[str, int] = Field(default_factory=dict)

class ThreatInfo(BaseModel):
    id: str
    filename: str
    threat_level: str
    threat_type: str
    detection_time: datetime
    details: Dict[str, Any]

# Global state
current_scan: Optional[ScanResult] = None
scan_history: List[ScanResult] = []
threats: List[ThreatInfo] = []

# Utility functions
def generate_scan_id():
    return f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

async def run_scan_pipeline(scan_request: ScanRequest, scan_id: str):
    """Execute the ThreatFusion scan pipeline"""
    global current_scan, threats
    
    current_scan = ScanResult(
        scan_id=scan_id,
        status=ScanStatus.RUNNING,
        start_time=datetime.now()
    )
    
    await manager.broadcast({
        "type": "scan_started",
        "scan_id": scan_id,
        "timestamp": datetime.now().isoformat()
    })
    
    try:
        # Import ThreatFusion components
        from run import compile_cpp_scanner, compile_advanced_scanner, run_cpp_scanner, run_advanced_scanner
        
        # Simulate scan progress
        steps = [
            ("Compiling C++ Scanner", 10),
            ("Scanning Files", 30),
            ("Network Analysis", 20),
            ("ML Analysis", 25),
            ("Generating Reports", 15)
        ]
        
        files_scanned = 0
        for step_name, duration in steps:
            await manager.broadcast({
                "type": "scan_progress",
                "scan_id": scan_id,
                "step": step_name,
                "timestamp": datetime.now().isoformat()
            })
            
            # Simulate work
            await asyncio.sleep(duration / 10)
            files_scanned += 10
            current_scan.files_scanned = files_scanned
        
        # Mock threat detection
        threat_levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        current_scan.threats_detected = files_scanned // 10
        current_scan.threat_summary = {
            "CRITICAL": 1,
            "HIGH": 2,
            "MEDIUM": 3,
            "LOW": 4
        }
        
        # Add mock threats
        for i in range(current_scan.threats_detected):
            threat = ThreatInfo(
                id=f"threat_{scan_id}_{i}",
                filename=f"suspicious_file_{i}.exe",
                threat_level=threat_levels[i % len(threat_levels)],
                threat_type="Malware Detection",
                detection_time=datetime.now(),
                details={
                    "entropy": 7.8,
                    "packed": True,
                    "suspicious_strings": ["CreateRemoteThread", "VirtualAllocEx"]
                }
            )
            threats.append(threat)
        
        current_scan.status = ScanStatus.COMPLETED
        current_scan.end_time = datetime.now()
        scan_history.append(current_scan)
        
        await manager.broadcast({
            "type": "scan_completed",
            "scan_id": scan_id,
            "threats_detected": current_scan.threats_detected,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        current_scan.status = ScanStatus.FAILED
        current_scan.end_time = datetime.now()
        await manager.broadcast({
            "type": "scan_failed",
            "scan_id": scan_id,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })

# API Endpoints

@app.get("/")
async def root():
    return {
        "name": "ThreatFusion API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/status")
async def get_status():
    """Get current system status"""
    return {
        "status": "operational",
        "current_scan": current_scan.dict() if current_scan else None,
        "total_scans": len(scan_history),
        "total_threats": len(threats),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/scan/start")
async def start_scan(scan_request: ScanRequest, background_tasks: BackgroundTasks):
    """Start a new security scan"""
    global current_scan
    
    if current_scan and current_scan.status == ScanStatus.RUNNING:
        raise HTTPException(status_code=400, detail="A scan is already running")
    
    scan_id = generate_scan_id()
    background_tasks.add_task(run_scan_pipeline, scan_request, scan_id)
    
    return {
        "message": "Scan started",
        "scan_id": scan_id,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/scan/current")
async def get_current_scan():
    """Get current scan status"""
    if not current_scan:
        return {"status": "idle", "message": "No active scan"}
    
    return current_scan.dict()

@app.get("/api/scan/history")
async def get_scan_history():
    """Get scan history"""
    return {
        "scans": [scan.dict() for scan in scan_history],
        "total": len(scan_history)
    }

@app.get("/api/threats")
async def get_threats(
    limit: int = 50,
    threat_level: Optional[str] = None
):
    """Get detected threats"""
    filtered_threats = threats
    
    if threat_level:
        filtered_threats = [t for t in threats if t.threat_level == threat_level]
    
    return {
        "threats": [t.dict() for t in filtered_threats[:limit]],
        "total": len(filtered_threats)
    }

@app.get("/api/threats/{threat_id}")
async def get_threat_details(threat_id: str):
    """Get detailed information about a specific threat"""
    threat = next((t for t in threats if t.id == threat_id), None)
    
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    return threat.dict()

@app.get("/api/statistics")
async def get_statistics():
    """Get overall statistics"""
    total_files = sum(scan.files_scanned for scan in scan_history)
    total_threats = len(threats)
    
    threat_by_level = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }
    
    for threat in threats:
        if threat.threat_level in threat_by_level:
            threat_by_level[threat.threat_level] += 1
    
    return {
        "total_scans": len(scan_history),
        "total_files_scanned": total_files,
        "total_threats_detected": total_threats,
        "threats_by_level": threat_by_level,
        "scan_success_rate": 0.95,
        "last_scan": scan_history[-1].dict() if scan_history else None
    }

@app.get("/api/reports")
async def list_reports():
    """List available reports"""
    reports_dir = project_root / "outputs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    reports = []
    for file_path in reports_dir.glob("*"):
        if file_path.is_file():
            reports.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "created": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "type": file_path.suffix[1:]
            })
    
    return {"reports": reports, "total": len(reports)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and receive messages
            data = await websocket.receive_text()
            # Echo back or process commands
            await websocket.send_json({
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            })
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        manager.disconnect(websocket)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
