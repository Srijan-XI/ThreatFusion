#!/bin/bash
# ThreatFusion Web Interface Startup Script (Linux/Mac)
# This script starts both the FastAPI backend and React frontend

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEB_DIR="$SCRIPT_DIR"
VENV_PATH="$SCRIPT_DIR/../../.venv"

echo -e "${CYAN}========================================"
echo -e "  ThreatFusion Web Interface"
echo -e "  Startup Script for Linux/Mac"
echo -e "========================================${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Node.js is installed
if ! command_exists node; then
    echo -e "${RED}[ERROR] Node.js is not installed!${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    echo ""
    exit 1
fi

# Check if npm is installed
if ! command_exists npm; then
    echo -e "${RED}[ERROR] npm is not installed!${NC}"
    echo "Please install npm (usually comes with Node.js)"
    echo ""
    exit 1
fi

# Check if Python is installed
if ! command_exists python3 && ! command_exists python; then
    echo -e "${RED}[ERROR] Python is not installed!${NC}"
    echo "Please install Python from https://python.org/"
    echo ""
    exit 1
fi

# Determine Python command
if command_exists python3; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Check if pip is installed
if ! command_exists pip3 && ! command_exists pip; then
    echo -e "${RED}[ERROR] pip is not installed!${NC}"
    echo "Please install pip"
    echo ""
    exit 1
fi

# Determine pip command
if command_exists pip3; then
    PIP_CMD="pip3"
else
    PIP_CMD="pip"
fi

# Check if npm dependencies are installed
if [ ! -d "$WEB_DIR/node_modules" ]; then
    echo -e "${YELLOW}[*] Installing npm dependencies...${NC}"
    echo ""
    cd "$WEB_DIR"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to install npm dependencies!${NC}"
        exit 1
    fi
fi

# Check if Python virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}[*] Virtual environment not found.${NC}"
    echo -e "${YELLOW}[*] Creating virtual environment...${NC}"
    cd "$SCRIPT_DIR/../.."
    $PYTHON_CMD -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to create virtual environment!${NC}"
        exit 1
    fi
fi

# Activate virtual environment and install Python dependencies
echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"
echo ""

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Install requirements
$PIP_CMD install -r "$WEB_DIR/api/requirements.txt" -q
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install Python dependencies!${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}========================================"
echo -e "  Starting Services"
echo -e "========================================${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}[*] Stopping services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}[*] Services stopped.${NC}"
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT SIGTERM

# Start Backend (FastAPI)
echo -e "${GREEN}[1/2] Starting FastAPI Backend...${NC}"
echo -e "      URL: ${BLUE}http://localhost:8000${NC}"
echo -e "      Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""

cd "$WEB_DIR/api"
source "$VENV_PATH/bin/activate"
uvicorn main:app --reload --port 8000 > /tmp/threatfusion-backend.log 2>&1 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR] Failed to start backend!${NC}"
    echo "Check logs at: /tmp/threatfusion-backend.log"
    exit 1
fi

# Start Frontend (React)
echo -e "${GREEN}[2/2] Starting React Frontend...${NC}"
echo -e "      URL: ${BLUE}http://localhost:3000${NC}"
echo ""

cd "$WEB_DIR"
npm run dev > /tmp/threatfusion-frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 3

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR] Failed to start frontend!${NC}"
    echo "Check logs at: /tmp/threatfusion-frontend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo -e "${GREEN}========================================"
echo -e "  Services Started Successfully!"
echo -e "========================================${NC}"
echo ""
echo -e "${CYAN}Frontend:${NC} http://localhost:3000"
echo -e "${CYAN}Backend:${NC}  http://localhost:8000"
echo -e "${CYAN}API Docs:${NC} http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Backend PID:${NC}  $BACKEND_PID"
echo -e "${YELLOW}Frontend PID:${NC} $FRONTEND_PID"
echo ""
echo -e "${GREEN}Both services are running.${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop all services.${NC}"
echo ""
echo "Logs are available at:"
echo "  Backend:  /tmp/threatfusion-backend.log"
echo "  Frontend: /tmp/threatfusion-frontend.log"
echo ""

# Try to open browser (works on most Linux desktop environments and macOS)
if command_exists xdg-open; then
    sleep 2
    xdg-open http://localhost:3000 2>/dev/null &
elif command_exists open; then
    sleep 2
    open http://localhost:3000 2>/dev/null &
fi

# Keep script running
echo -e "${CYAN}Waiting for services... (Ctrl+C to stop)${NC}"
wait
