# Advanced C++ Scanner - ThreatFusion

## Overview

The Advanced C++ Scanner is a comprehensive malware analysis and threat detection system that performs deep executable analysis, entropy calculation, hash-based detection, and behavioral analysis.

## Features

### 🔍 **Deep Executable Analysis**
- **PE (Portable Executable) Parser**: Analyzes Windows executables
  - Extracts COFF header information
  - Parses optional header
  - Enumerates sections
  - Identifies imports and suspicious API calls
- **ELF (Executable and Linkable Format) Parser**: Analyzes Linux executables
  - Detects 32-bit vs 64-bit binaries
  - Identifies target architecture
  - Extracts entry point information

### 🧬 **Entropy Analysis**
- Calculates Shannon entropy to detect packed/encrypted malware
- Configurable entropy threshold (default: 7.0)
- High entropy indicates potential packing or encryption

### 🔐 **Hash-Based Detection**
- Calculates MD5, SHA1, and SHA256 hashes
- Compares against known malware hash database
- Supports custom hash databases

### 🧵 **String Extraction & Analysis**
- Extracts printable strings from binaries
- Identifies suspicious API calls and function names
- Extracts URLs, IP addresses, and email addresses
- Detects command-line tools and scripts

### 🛡️ **Threat Detection**
- **Packer Detection**: Identifies UPX, ASPack, Themida, PECompact, FSG, and more
- **Anti-Debug Detection**: Detects anti-debugging techniques
- **Shellcode Detection**: Identifies common shellcode patterns
- **Exploit Detection**: Detects NOP sleds and suspicious byte sequences
- **Suspicious Imports**: Flags dangerous API calls

### 📊 **Threat Assessment**
Multi-level threat classification:
- **CRITICAL**: Severe threats requiring immediate attention
- **HIGH**: Significant security risks
- **MEDIUM**: Moderate threats
- **LOW**: Minor suspicious indicators
- **NONE**: Clean files

### 📄 **Comprehensive Reporting**
- **JSON Reports**: Machine-readable detailed analysis
- **Text Reports**: Human-readable summaries
- **Real-time Logging**: Live scan progress and threat detection

## Compilation

### Prerequisites
- C++17 compatible compiler (g++, clang++, MSVC)
- nlohmann/json library (included as json.hpp)

### Build Commands

#### Windows (MinGW/MSVC)
```bash
# Using g++
g++ -std=c++17 -O2 -o advanced_scanner.exe scanner_cpp/advanced_main.cpp scanner_cpp/advanced_scanner.cpp -I scanner_cpp

# Using MSVC
cl /std:c++17 /O2 /EHsc scanner_cpp/advanced_main.cpp scanner_cpp/advanced_scanner.cpp /I scanner_cpp /Fe:advanced_scanner.exe
```

#### Linux
```bash
g++ -std=c++17 -O2 -o advanced_scanner scanner_cpp/advanced_main.cpp scanner_cpp/advanced_scanner.cpp -I scanner_cpp
```

#### macOS
```bash
clang++ -std=c++17 -O2 -o advanced_scanner scanner_cpp/advanced_main.cpp scanner_cpp/advanced_scanner.cpp -I scanner_cpp
```

## Usage

### Basic Usage
```bash
# Scan default directory (data/samples)
./advanced_scanner

# Scan specific directory
./advanced_scanner --target /path/to/scan

# Custom log file
./advanced_scanner --log /path/to/logfile.log
```

### Advanced Options
```bash
# Disable specific features
./advanced_scanner --no-deep          # Disable deep executable analysis
./advanced_scanner --no-hash          # Disable hash calculation
./advanced_scanner --no-entropy       # Disable entropy analysis
./advanced_scanner --no-strings       # Disable string extraction

# Adjust entropy threshold
./advanced_scanner --entropy-threshold 7.5

# Combine options
./advanced_scanner --target samples/ --no-hash --entropy-threshold 6.5
```

### Help
```bash
./advanced_scanner --help
```

## Configuration Files

### 1. **rules.json** - Signature Database
Located at: `configs/rules.json`

Contains byte patterns for:
- File type identification
- Packer detection
- Malware signatures
- Exploit patterns
- Shellcode detection

Example:
```json
{
  "signatures": [
    {
      "pattern": "4d5a",
      "description": "PE executable",
      "severity": "info"
    },
    {
      "pattern": "5550582100000000",
      "description": "UPX packer detected",
      "severity": "high"
    }
  ]
}
```

### 2. **malware_hashes.json** - Known Malware Hashes
Located at: `configs/malware_hashes.json`

Contains MD5, SHA1, and SHA256 hashes of known malware.

Example:
```json
{
  "hashes": [
    "44d88612fea8a8f36de82e1278abb02f",
    "3395856ce81f2b7382dee72602f798b642f14140"
  ]
}
```

### 3. **suspicious_strings.txt** - Suspicious String Database
Located at: `configs/suspicious_strings.txt`

Contains suspicious API calls, executables, and function names.

Example:
```
CreateRemoteThread
VirtualAllocEx
WriteProcessMemory
cmd.exe
powershell.exe
```

## Output Files

### Log File
Default: `outputs/logs/advanced_scan.log`

Contains real-time scan results with timestamps and threat details.

### JSON Report
Default: `outputs/reports/advanced_scan_report.json`

Machine-readable detailed analysis including:
- File paths and metadata
- Threat levels and classifications
- Hash values
- Extracted indicators (URLs, IPs, emails)
- Detection reasons

### Text Report
Default: `outputs/reports/advanced_scan_report.txt`

Human-readable summary with:
- Scan statistics
- Threat breakdown by severity
- Detailed threat analysis

## Architecture

### Class Structure

```
AdvancedScanner
├── Configuration
│   ├── setDeepScan()
│   ├── setHashCheck()
│   ├── setEntropyAnalysis()
│   └── setStringExtraction()
├── Loading
│   ├── loadSignatures()
│   ├── loadMalwareHashes()
│   └── loadSuspiciousStrings()
├── Analysis
│   ├── detectFileType()
│   ├── calculateEntropy()
│   ├── calculateHashes()
│   ├── extractStrings()
│   ├── analyzePE()
│   ├── analyzeELF()
│   └── assessThreatLevel()
├── Scanning
│   ├── scanFile()
│   └── scanDirectory()
└── Reporting
    ├── generateJSONReport()
    └── generateTextReport()
```

### Data Structures

- **FileAnalysis**: Complete analysis results for a single file
- **PEHeader**: PE executable header information
- **ELFHeader**: ELF executable header information
- **FileHashes**: MD5, SHA1, SHA256 hash values
- **ScanResult**: Aggregated scan results for entire directory

## Detection Capabilities

### File Types Detected
- PE Executables (Windows)
- ELF Executables (Linux)
- Java Class Files
- Archives (ZIP, RAR, 7-Zip, GZIP, BZIP2)
- Documents (PDF, Microsoft Office)
- Images (PNG, JPEG)

### Packers Detected
- UPX
- ASPack
- Themida/WinLicense
- PECompact
- FSG
- Petite

### Malware Indicators
- High entropy (packing/encryption)
- Anti-debugging techniques
- Suspicious API imports
- Shellcode patterns
- NOP sleds
- Reverse shell patterns
- Command execution patterns

## Performance Considerations

- **Memory Usage**: Files are loaded into memory for analysis
- **Scan Speed**: ~100-500 files/second depending on file size and enabled features
- **Optimization**: Disable unnecessary features for faster scanning

## Integration with ThreatFusion

The advanced scanner integrates seamlessly with the ThreatFusion platform:

```python
# From run.py
def compile_advanced_scanner():
    subprocess.run([
        "g++", "-std=c++17", "-O2",
        "-o", "scanner_cpp/advanced_scanner.exe",
        "scanner_cpp/advanced_main.cpp",
        "scanner_cpp/advanced_scanner.cpp"
    ])

def run_advanced_scanner():
    subprocess.run(["scanner_cpp/advanced_scanner.exe"])
```

## Future Enhancements

- [ ] YARA rules integration
- [ ] Sandbox integration (Cuckoo, Any.Run)
- [ ] VirusTotal API integration
- [ ] Real-time hash calculation using OpenSSL
- [ ] Parallel file scanning
- [ ] Memory-mapped file I/O for large files
- [ ] Plugin system for custom analyzers
- [ ] Machine learning-based classification

## Troubleshooting

### Common Issues

**Issue**: Compilation errors with json.hpp
- **Solution**: Ensure nlohmann/json library is in the include path

**Issue**: High false positive rate
- **Solution**: Adjust entropy threshold or disable specific detection methods

**Issue**: Slow scanning
- **Solution**: Disable deep scan or string extraction for faster results

**Issue**: Missing configuration files
- **Solution**: Ensure all config files exist in `configs/` directory

## Contributing

To add new signatures:
1. Edit `configs/rules.json`
2. Add hex pattern and description
3. Set appropriate severity level

To add malware hashes:
1. Edit `configs/malware_hashes.json`
2. Add MD5, SHA1, or SHA256 hashes

## License

Part of the ThreatFusion project - Advanced Cybersecurity Analysis Platform

## Credits

Developed as part of ThreatFusion's enhanced C++ scanner module.

---

**Note**: This scanner is for educational and authorized security testing purposes only. Always obtain proper authorization before scanning systems.
