# ThreatFusion: Unified Cybersecurity Analysis Platform

## Overview

ThreatFusion is a modular cybersecurity project designed to perform multi-layered threat detection through an integrated tech stack utilizing C++, Python, and Go.  
It leverages network scanning, heuristic log analysis, and behavioral detection to provide a comprehensive security posture assessment.

This project respects traditional cybersecurity principles while embracing modern automation and cross-language interoperability to deliver scalable and efficient threat intelligence.

---

## Project Structure
```
ThreatFusion/
├── analyzer_py/ # Python module for log analysis and heuristics
│ ├── init.py
│ ├── analyzer.py
│ └── models/
│ ├── init.py
│ └── heuristics.py
├── scanner_cpp/ # C++ based network scanner
│ ├── main.cpp
│ ├── scanner.hpp
│ └── utils.cpp
├── net_analyzer_go/ # Go-based network analysis tool
│ └── netscan.go
├── outputs/
│ └── logs/ # Directory for input log files
└── README.md # Project documentation
```

---

## Prerequisites

- C++ compiler supporting C++17 standard (e.g., `g++`)
- Python 3.8+ (tested with Python 3.13.7)
- Go programming language environment (for Go tools)
- Required Python packages: pandas, matplotlib, fpdf, scikit-learn

---

## Setup & Usage

### Python Log Analyzer

1. Place `.log` files to analyze inside `outputs/logs/`.
2. Run the analyzer module from the project root:

```bash
python -m analyzer_py.analyzer
```
Review the terminal output for suspicious log entries flagged by heuristics.

C++ Scanner (Planned)
Compile and run the scanner in scanner_cpp/.

Integrate output logs with Python analyzer for deeper inspection.

Go Network Analyzer (Planned)
- Build and run the Go ```netscan.go```.

- Feed network scan results into the Python analysis pipeline.

- Project Vision & Next Steps
Expand heuristic detection rules with machine learning techniques.

- Automate pipeline for continuous monitoring and alerting.

- Implement secure communication between C++, Go, and Python modules.

- Document usage cases and threat scenarios for operational readiness.

***Contribution & Contact***

This project honors the discipline and legacy of cybersecurity professionals and invites contributions that uphold these standards.# ThreatFusion
