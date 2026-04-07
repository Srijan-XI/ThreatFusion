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