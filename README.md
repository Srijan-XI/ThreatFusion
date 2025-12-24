# ThreatFusion: Unified Cybersecurity Analysis Platform

## 🛡️ Overview

**ThreatFusion** is a comprehensive, multi-layered cybersecurity analysis platform that combines the power of C++, Python, and Go to deliver enterprise-grade threat detection and analysis. With an integrated **web interface**, real-time monitoring, and advanced reporting capabilities, ThreatFusion provides a complete solution for modern security operations.

### Key Features
- 🔍 **Advanced Malware Detection** - PE/ELF parsing, entropy analysis, signature matching
- 🌐 **Network Analysis** - Packet capture, protocol analysis, traffic anomaly detection
- 🚨 **Real-time Monitoring** - WebSocket-based live threat updates
- 📊 **Interactive Web Dashboard** - Modern React-based interface
- 📈 **Comprehensive Reporting** - HTML, PDF, Excel, CSV export
- 🤖 **ML Integration** - Machine learning-based anomaly detection
- 🔌 **RESTful API** - FastAPI backend with full documentation

---

## 🚀 Quick Start

### Web Interface (Recommended)

**Windows:**
```batch
cd web
run.bat
```

**Linux/Mac:**
```bash
cd web
chmod +x run.sh
./run.sh
```

Access the dashboard at **http://localhost:3000**

### Command Line
```bash
python run.py
```

---

## 📁 Project Structure

```
ThreatFusion/
├── web/                      # Web Interface (NEW!)
│   ├── api/                  # FastAPI Backend
│   │   ├── main.py          # REST API + WebSocket
│   │   └── requirements.txt
│   ├── src/                  # React Frontend
│   │   ├── components/      # UI Components
│   │   ├── pages/           # Dashboard, Scans, Threats, Reports, Settings
│   │   └── services/        # API Client + WebSocket
│   ├── run.bat              # Windows startup script
│   ├── run.sh               # Linux/Mac startup script
│   └── package.json
│
├── scanner_cpp/              # C++ Advanced Scanner
│   ├── advanced_scanner.cpp # PE/ELF parser, entropy analysis
│   ├── advanced_scanner.hpp # Header definitions
│   └── advanced_main.cpp    # Scanner entry point
│
├── net_analyzer_go/          # Go Network Scanner
│   └── netscan.go           # Concurrent network scanning
│
├── analyzer_py/              # Python Analysis Engine
│   ├── analyzer.py          # Main analyzer
│   └── models/
│       └── heuristics.py    # Detection heuristics
│
├── core/                     # Core Modules
│   ├── logger.py            # Advanced logging system
│   ├── error_handler.py     # Error handling & recovery
│   └── reporting.py         # Multi-format reporting
│
├── network/                  # Network Analysis
│   └── network_analyzer.py  # Packet capture & analysis
│
├── configs/                  # Configuration Files
│   ├── rules.json           # Signature database
│   ├── malware_hashes.json  # Known malware hashes
│   └── suspicious_strings.txt
│
├── data/                     # Test Data
│   └── samples/             # Sample files for testing
│
├── outputs/                  # Output Directory
│   ├── logs/                # Log files
│   └── reports/             # Generated reports
│
├── run.py                    # Main orchestrator
└── requirements.txt          # Python dependencies
```

---

## 🌐 Web Interface

### Features
- **🏠 Dashboard** - Real-time statistics, threat visualization, system status
- **🔍 Scans** - Configure scans, upload files, monitor progress, view history
- **⚠️ Threats** - Filter threats, detailed analysis, export to CSV
- **📄 Reports** - Generate and download reports in multiple formats
- **⚙️ Settings** - Configure scanners, notifications, API keys, system settings

### Technology Stack
- **Frontend**: React 18, Vite, Tailwind CSS, Chart.js
- **Backend**: FastAPI, WebSockets, Uvicorn
- **Design**: Glassmorphism, Dark theme, Responsive

### Access Points
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Startup Scripts
-**Windows**: `web/run.bat` - One-click startup
- **Linux/Mac**: `web/run.sh` - Bash script with auto-cleanup
- **PowerShell**: `web/start-all.ps1` - PowerShell alternative

---

## 🔧 Prerequisites

### Required Software
- **Node.js** 18+ (for web interface)
- **Python** 3.8+ (tested with 3.13.7)
- **C++** compiler supporting C++17 (g++, clang++, MSVC)
- **Go** 1.16+ (for network scanner)

### Python Dependencies
```bash
pip install -r requirements.txt
```

**Core Packages:**
- pandas >= 1.5.0
- matplotlib >= 3.5.0
- fpdf >= 1.7.2
- scikit-learn >= 1.0.0
- scapy >= 2.5.0
- fastapi >= 0.110.0
- uvicorn >= 0.27.0

### Web Interface Dependencies
```bash
cd web
npm install
```

---

## 💻 Usage

### 1. Web Interface (Easiest)

**Start everything:**
```batch
cd web
run.bat          # Windows
./run.sh         # Linux/Mac
```

**Open browser:**
- Navigate to http://localhost:3000
- Click "Start Quick Scan"
- Monitor real-time results
- View threats and reports

### 2. Command Line (Traditional)

**Run complete analysis:**
```bash
python run.py
```

**Run specific components:**
```bash
# C++ Scanner
cd scanner_cpp
g++ -std=c++17 -O2 -o advanced_scanner advanced_main.cpp advanced_scanner.cpp
./advanced_scanner ../data/samples

# Go Network Scanner
cd net_analyzer_go
go run netscan.go

# Python Analyzer
python -m analyzer_py.analyzer
```

### 3. API Integration

**Start API server:**
```bash
cd web/api
uvicorn main:app --reload --port 8000
```

**API endpoints:**
```python
import requests

# Start scan
response = requests.post('http://localhost:8000/api/scan/start', json={
    'target_directory': 'data/samples',
    'scan_type': 'full',
    'enable_ml': True
})

# Get threats
threats = requests.get('http://localhost:8000/api/threats').json()

# Generate report
reports = requests.get('http://localhost:8000/api/reports').json()
```

---

## 📊 Features

### Advanced Malware Detection
- ✅ PE/ELF executable parsing
- ✅ Entropy analysis for packer detection
- ✅ 34+ signature database
- ✅ Hash-based malware identification
- ✅ String extraction and analysis
- ✅ Anti-debug technique detection
- ✅ 5-level threat classification

### Network Analysis
- ✅ Packet capture with Scapy
- ✅ Protocol analysis (HTTP, DNS, TLS)
- ✅ Traffic anomaly detection
- ✅ Port scan detection
- ✅ DDoS detection
- ✅ IP geolocation
- ✅ Threat intelligence integration

### Reporting & Logging
- ✅ HTML interactive dashboards
- ✅ PDF executive summaries
- ✅ Excel workbooks with multiple sheets
- ✅ CSV exports for SIEM integration
- ✅ Structured JSON logging
- ✅ Real-time WebSocket updates

### Web Features
- ✅ Real-time threat monitoring
- ✅ File upload for scanning
- ✅ Advanced filtering and search
- ✅ Export functionality
- ✅ Configurable settings
- ✅ Notification system (Email, Discord, Telegram)
- ✅ API key management

---

## 🎯 Use Cases

### Security Operations Center (SOC)
- Real-time threat monitoring dashboard
- Automated alert generation
- Multi-format reporting for different stakeholders

### Incident Response
- Quick malware analysis
- Network traffic investigation
- Detailed threat intelligence

### Malware Research
- Deep file analysis
- Pattern signature development
- Threat family classification

### Compliance & Auditing
- Automated security scanning
- Comprehensive audit reports
- Historical data tracking

---

## 📚 Documentation

- **`web/README.md`** - Web interface documentation
- **`web/QUICKSTART.md`** - Quick start guide
- **`web/FEATURE_GUIDE.md`** - Complete feature reference
- **`scanner_cpp/README_ADVANCED.md`** - C++ scanner guide
- **`CHANGELOG.md`** - Version history and updates

---

## 🛠️ Configuration

### Scanner Settings
Edit `configs/rules.json` for signature updates:
```json
{
  "signatures": [
    {
      "name": "UPX Packer",
      "pattern": "555058",
      "offset": 0,
      "type": "packer"
    }
  ]
}
```

### Web Interface Settings
Access via **Settings page** (http://localhost:3000/settings):
- Scanner configuration
- Notification preferences
- API keys (VirusTotal, AbuseIPDB)
- System parameters

---

## 🔐 Security

### API Keys (Optional)
Configure in Settings page:
- **VirusTotal** - Enhanced threat intelligence
- **AbuseIPDB** - IP reputation checking

### Notifications
Setup alerts via:
- **Email** - SMTP configuration
- **Discord** - Webhook URL
- **Telegram** - Bot token & chat ID

---

## 📈 Performance

- **Scanning Speed**: ~1000 files/second (small files < 1MB)
- **Network Analysis**: Real-time packet processing
- **Web Interface**: Responsive with WebSocket updates
- **API Response**: < 100ms for most endpoints

---

## 🤝 Contributing

This project honors the discipline and legacy of cybersecurity professionals. Contributions that uphold these standards are welcome.

---

## 📄 License

Proprietary software developed for cybersecurity research and analysis.

---

## 👤 Author

**Srijan** - Lead Developer & Architect

---

## 🎯 Version

**Current Version**: 3.0.0 (Web Interface Release)

See `CHANGELOG.md` for detailed version history.

---

## 🚀 Getting Started Checklist

- [ ] Install Node.js, Python, C++, Go
- [ ] Clone repository
- [ ] Install Python dependencies (`pip install -r requirements.txt`)
- [ ] Install web dependencies (`cd web && npm install`)
- [ ] Run web interface (`cd web && run.bat` or `./run.sh`)
- [ ] Access dashboard (http://localhost:3000)
- [ ] Start first scan
- [ ] Explore features

---

**For quick start, see: `web/QUICKSTART.md`**

**For detailed features, see: `web/FEATURE_GUIDE.md`**

**Made with ❤️ for cybersecurity professionals**
