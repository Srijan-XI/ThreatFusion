#include <iostream>
#include <string>
#include "advanced_scanner.hpp"

void printBanner() {
    std::cout << R"(
╔═══════════════════════════════════════════════════════════╗
║         ThreatFusion Advanced C++ Scanner v2.0            ║
║     Deep Malware Analysis & Threat Detection System       ║
╚═══════════════════════════════════════════════════════════╝
)" << std::endl;
}

void printHelp() {
    std::cout << "Usage: advanced_scanner [options]" << std::endl;
    std::cout << "\nOptions:" << std::endl;
    std::cout << "  --target <dir>       Target directory to scan (default: data/samples)" << std::endl;
    std::cout << "  --log <file>         Log file path (default: outputs/logs/advanced_scan.log)" << std::endl;
    std::cout << "  --no-deep            Disable deep executable analysis" << std::endl;
    std::cout << "  --no-hash            Disable hash calculation" << std::endl;
    std::cout << "  --no-entropy         Disable entropy analysis" << std::endl;
    std::cout << "  --no-strings         Disable string extraction" << std::endl;
    std::cout << "  --entropy-threshold  Set entropy threshold (default: 7.0)" << std::endl;
    std::cout << "  --help               Show this help message" << std::endl;
    std::cout << std::endl;
}

int main(int argc, char* argv[]) {
    printBanner();

    // Default configuration
    std::string targetDir = "data/samples";
    std::string logFile = "outputs/logs/advanced_scan.log";
    bool enableDeepScan = true;
    bool enableHashCheck = true;
    bool enableEntropyAnalysis = true;
    bool enableStringExtraction = true;
    double entropyThreshold = 7.0;

    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        
        if (arg == "--help" || arg == "-h") {
            printHelp();
            return 0;
        } else if (arg == "--target" && i + 1 < argc) {
            targetDir = argv[++i];
        } else if (arg == "--log" && i + 1 < argc) {
            logFile = argv[++i];
        } else if (arg == "--no-deep") {
            enableDeepScan = false;
        } else if (arg == "--no-hash") {
            enableHashCheck = false;
        } else if (arg == "--no-entropy") {
            enableEntropyAnalysis = false;
        } else if (arg == "--no-strings") {
            enableStringExtraction = false;
        } else if (arg == "--entropy-threshold" && i + 1 < argc) {
            entropyThreshold = std::stod(argv[++i]);
        }
    }

    // Create scanner instance
    AdvancedScanner scanner(targetDir, logFile);

    // Configure scanner
    scanner.setDeepScan(enableDeepScan);
    scanner.setHashCheck(enableHashCheck);
    scanner.setEntropyAnalysis(enableEntropyAnalysis);
    scanner.setStringExtraction(enableStringExtraction);
    scanner.setEntropyThreshold(entropyThreshold);

    // Load configurations
    std::cout << "[*] Loading threat intelligence..." << std::endl;
    scanner.loadSignatures("configs/rules.json");
    scanner.loadMalwareHashes("configs/malware_hashes.json");
    scanner.loadSuspiciousStrings("configs/suspicious_strings.txt");
    std::cout << std::endl;

    // Perform scan
    ScanResult result = scanner.scanDirectory();

    // Generate reports
    std::cout << "\n[*] Generating reports..." << std::endl;
    scanner.generateJSONReport(result);
    scanner.generateTextReport(result);

    // Print summary
    std::cout << "\n" << std::string(60, '=') << std::endl;
    std::cout << "SCAN SUMMARY" << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    std::cout << "Total Files Scanned: " << result.totalFilesScanned << std::endl;
    std::cout << "Threats Detected: " << result.threatsDetected << std::endl;
    
    if (!result.threatsByLevel.empty()) {
        std::cout << "\nThreat Breakdown:" << std::endl;
        for (const auto& [level, count] : result.threatsByLevel) {
            std::cout << "  " << scanner.getThreatLevelString(level) << ": " << count << std::endl;
        }
    }
    
    std::cout << std::string(60, '=') << std::endl;

    if (result.threatsDetected > 0) {
        std::cout << "\n[!] THREATS DETECTED - Review reports for details" << std::endl;
        return 1;
    } else {
        std::cout << "\n[+] No threats detected - System appears clean" << std::endl;
        return 0;
    }
}
