@echo off
REM ThreatFusion Web Interface Startup Script (Windows)
REM This script starts both the FastAPI backend and React frontend

color 0A
echo ========================================
echo   ThreatFusion Web Interface
echo   Startup Script for Windows
echo ========================================
echo.

REM Store the web directory path
set WEB_DIR=%~dp0

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR] Python is not installed!
    echo Please install Python from https://python.org/
    echo.
    pause
    exit /b 1
)

REM Check if npm dependencies are installed
if not exist "%WEB_DIR%node_modules" (
    echo [*] Installing npm dependencies...
    echo.
    cd "%WEB_DIR%"
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        color 0C
        echo [ERROR] Failed to install npm dependencies!
        pause
        exit /b 1
    )
)

REM Check if Python virtual environment exists
set VENV_PATH=%WEB_DIR%..\..\.venv
if not exist "%VENV_PATH%" (
    echo [*] Virtual environment not found.
    echo [*] Creating virtual environment...
    cd "%WEB_DIR%.."
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        color 0C
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
)

REM Install Python dependencies
echo [*] Installing Python dependencies...
echo.
call "%VENV_PATH%\Scripts\activate.bat"
pip install -r "%WEB_DIR%api\requirements.txt" -q
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR] Failed to install Python dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Starting Services
echo ========================================
echo.

REM Start Backend (FastAPI) in a new window
echo [1/2] Starting FastAPI Backend...
echo       URL: http://localhost:8000
echo       Docs: http://localhost:8000/docs
echo.
start "ThreatFusion API Backend" cmd /k "cd /d "%WEB_DIR%api" && "%VENV_PATH%\Scripts\activate.bat" && uvicorn main:app --reload --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend (React) in a new window
echo [2/2] Starting React Frontend...
echo       URL: http://localhost:3000
echo.
start "ThreatFusion Web Frontend" cmd /k "cd /d "%WEB_DIR%" && npm run dev"

REM Wait a bit for frontend to start
timeout /t 3 /nobreak >nul

echo.
color 0B
echo ========================================
echo   Services Started Successfully!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Both services are running in separate windows.
echo Close those windows to stop the services.
echo.
echo Opening browser in 3 seconds...
echo.

REM Wait and open browser
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo Press any key to exit this window...
pause >nul
