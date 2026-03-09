#include "advanced_scanner.hpp"
#include "json.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <chrono>
#include <regex>
#include <cstring>

// For hash calculations (simplified - in production use OpenSSL or similar)
#include <functional>

namespace fs = std::filesystem;
using json = nlohmann::json;

// ==================== Constructor & Destructor ====================

AdvancedScanner::AdvancedScanner(const std::string& dir, const std::string& log)
    : targetDir(dir), logFile(log), reportFile("outputs/reports/advanced_scan_report.json"),
      enableDeepScan(true), enableHashCheck(true), enableEntropyAnalysis(true),
      enableStringExtraction(true), entropyThreshold(7.0), filesScanned(0), threatsFound(0) {
    
    // Initialize suspicious strings database
    suspiciousStrings = {
        "cmd.exe", "powershell.exe", "eval", "exec", "system",
        "CreateRemoteThread", "VirtualAllocEx", "WriteProcessMemory",
        "IsDebuggerPresent", "CheckRemoteDebuggerPresent",
        "GetProcAddress", "LoadLibrary", "WinExec", "ShellExecute"
    };
}

AdvancedScanner::~AdvancedScanner() {
    // Cleanup if needed
}

// ==================== Configuration Methods ====================

void AdvancedScanner::setDeepScan(bool enable) { enableDeepScan = enable; }
void AdvancedScanner::setHashCheck(bool enable) { enableHashCheck = enable; }
void AdvancedScanner::setEntropyAnalysis(bool enable) { enableEntropyAnalysis = enable; }
void AdvancedScanner::setStringExtraction(bool enable) { enableStringExtraction = enable; }
void AdvancedScanner::setEntropyThreshold(double threshold) { entropyThreshold = threshold; }

// ==================== Loading Methods ====================

void AdvancedScanner::loadSignatures(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file) {
        std::cerr << "[-] Unable to open signature file: " << filepath << std::endl;
        return;
    }

    try {
        json j;
        file >> j;
        for (const auto& sig : j["signatures"]) {
            signatures[sig["pattern"]] = sig["description"];
        }
        std::cout << "[+] Loaded " << signatures.size() << " signatures" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "[-] Error parsing signatures: " << e.what() << std::endl;
    }
}

void AdvancedScanner::loadMalwareHashes(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file) {
        std::cout << "[*] No malware hash database found (optional)" << std::endl;
        return;
    }

    try {
        json j;
        file >> j;
        for (const auto& hash : j["hashes"]) {
            knownMalwareHashes.insert(hash.get<std::string>());
        }
        std::cout << "[+] Loaded " << knownMalwareHashes.size() << " known malware hashes" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "[-] Error loading malware hashes: " << e.what() << std::endl;
    }
}

void AdvancedScanner::loadSuspiciousStrings(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file) {
        std::cout << "[*] Using default suspicious strings database" << std::endl;
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty()) {
            suspiciousStrings.insert(line);
        }
    }
    std::cout << "[+] Loaded " << suspiciousStrings.size() << " suspicious strings" << std::endl;
}

// ==================== File Type Detection ====================

FileType AdvancedScanner::detectFileType(const std::vector<uint8_t>& data) {
    if (data.size() < 4) return FileType::UNKNOWN;

    // Check PE (MZ header)
    if (data[0] == 0x4D && data[1] == 0x5A) {
        return FileType::PE_EXECUTABLE;
    }

    // Check ELF (0x7F 'E' 'L' 'F')
    if (data[0] == 0x7F && data[1] == 0x45 && data[2] == 0x4C && data[3] == 0x46) {
        return FileType::ELF_EXECUTABLE;
    }

    // Check ZIP/JAR
    if (data[0] == 0x50 && data[1] == 0x4B && data[2] == 0x03 && data[3] == 0x04) {
        return FileType::ARCHIVE;
    }

    // Check PNG
    if (data.size() >= 8 && data[0] == 0x89 && data[1] == 0x50 && data[2] == 0x4E && data[3] == 0x47) {
        return FileType::IMAGE;
    }

    // Check PDF
    if (data.size() >= 4 && data[0] == 0x25 && data[1] == 0x50 && data[2] == 0x44 && data[3] == 0x46) {
        return FileType::DOCUMENT;
    }

    return FileType::BINARY;
}

// ==================== Entropy Calculation ====================

double AdvancedScanner::calculateEntropy(const std::vector<uint8_t>& data) {
    if (data.empty()) return 0.0;

    // Count byte frequencies
    std::map<uint8_t, int> frequencies;
    for (uint8_t byte : data) {
        frequencies[byte]++;
    }

    // Calculate Shannon entropy
    double entropy = 0.0;
    double dataSize = static_cast<double>(data.size());

    for (const auto& [byte, count] : frequencies) {
        double probability = count / dataSize;
        entropy -= probability * std::log2(probability);
    }

    return entropy;
}

// ==================== Hash Calculation ====================

FileHashes AdvancedScanner::calculateHashes(const std::vector<uint8_t>& data) {
    FileHashes hashes;
    
    // Simplified hash calculation (in production, use OpenSSL or similar)
    // For demonstration, we'll use std::hash
    std::hash<std::string> hasher;
    std::string dataStr(data.begin(), data.end());
    
    // These are placeholder implementations - replace with actual crypto hashes
    hashes.md5 = ScannerUtils::md5Hash(data);
    hashes.sha1 = ScannerUtils::sha1Hash(data);
    hashes.sha256 = ScannerUtils::sha256Hash(data);
    
    return hashes;
}

// ==================== String Extraction ====================

std::vector<std::string> AdvancedScanner::extractStrings(const std::vector<uint8_t>& data, size_t minLength) {
    std::vector<std::string> strings;
    std::string currentString;

    for (uint8_t byte : data) {
        if (std::isprint(byte)) {
            currentString += static_cast<char>(byte);
        } else {
            if (currentString.length() >= minLength) {
                strings.push_back(currentString);
            }
            currentString.clear();
        }
    }

    // Add last string if valid
    if (currentString.length() >= minLength) {
        strings.push_back(currentString);
    }

    return strings;
}

std::vector<std::string> AdvancedScanner::extractURLs(const std::string& content) {
    std::vector<std::string> urls;
    std::regex urlPattern(R"((https?|ftp)://[^\s/$.?#].[^\s]*)");
    
    auto begin = std::sregex_iterator(content.begin(), content.end(), urlPattern);
    auto end = std::sregex_iterator();
    
    for (auto it = begin; it != end; ++it) {
        urls.push_back(it->str());
    }
    
    return urls;
}

std::vector<std::string> AdvancedScanner::extractIPAddresses(const std::string& content) {
    std::vector<std::string> ips;
    std::regex ipPattern(R"(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)");
    
    auto begin = std::sregex_iterator(content.begin(), content.end(), ipPattern);
    auto end = std::sregex_iterator();
    
    for (auto it = begin; it != end; ++it) {
        ips.push_back(it->str());
    }
    
    return ips;
}

std::vector<std::string> AdvancedScanner::extractEmails(const std::string& content) {
    std::vector<std::string> emails;
    std::regex emailPattern(R"(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)");
    
    auto begin = std::sregex_iterator(content.begin(), content.end(), emailPattern);
    auto end = std::sregex_iterator();
    
    for (auto it = begin; it != end; ++it) {
        emails.push_back(it->str());
    }
    
    return emails;
}

// ==================== PE Analysis ====================

std::shared_ptr<PEHeader> AdvancedScanner::analyzePE(const std::vector<uint8_t>& data) {
    auto peHeader = std::make_shared<PEHeader>();
    peHeader->isValid = false;

    if (data.size() < 64) return peHeader;

    // Check MZ signature
    if (data[0] != 0x4D || data[1] != 0x5A) return peHeader;

    // Get PE header offset (at offset 0x3C)
    uint32_t peOffset = *reinterpret_cast<const uint32_t*>(&data[0x3C]);
    
    if (peOffset + 24 > data.size()) return peHeader;

    // Check PE signature
    if (data[peOffset] != 0x50 || data[peOffset + 1] != 0x45) return peHeader;

    peHeader->isValid = true;
    
    // Parse COFF header
    peHeader->machine = *reinterpret_cast<const uint16_t*>(&data[peOffset + 4]);
    peHeader->numberOfSections = *reinterpret_cast<const uint16_t*>(&data[peOffset + 6]);
    peHeader->timeDateStamp = *reinterpret_cast<const uint32_t*>(&data[peOffset + 8]);
    peHeader->characteristics = *reinterpret_cast<const uint32_t*>(&data[peOffset + 20]);

    // Parse optional header (simplified)
    if (peOffset + 24 + 2 < data.size()) {
        uint16_t magic = *reinterpret_cast<const uint16_t*>(&data[peOffset + 24]);
        
        // Check if PE32 (0x10B) or PE32+ (0x20B)
        if (magic == 0x10B || magic == 0x20B) {
            // Extract subsystem and image base (simplified)
            if (peOffset + 24 + 68 < data.size()) {
                peHeader->subsystem = *reinterpret_cast<const uint16_t*>(&data[peOffset + 24 + 68]);
            }
        }
    }

    // Extract section names (simplified)
    size_t sectionTableOffset = peOffset + 24 + 
        *reinterpret_cast<const uint16_t*>(&data[peOffset + 20]); // Size of optional header
    
    for (int i = 0; i < peHeader->numberOfSections && sectionTableOffset + 40 * (i + 1) <= data.size(); i++) {
        size_t sectionOffset = sectionTableOffset + 40 * i;
        std::string sectionName(reinterpret_cast<const char*>(&data[sectionOffset]), 8);
        sectionName = sectionName.c_str(); // Trim at null terminator
        peHeader->sections.push_back(sectionName);
    }

    return peHeader;
}

// ==================== ELF Analysis ====================

std::shared_ptr<ELFHeader> AdvancedScanner::analyzeELF(const std::vector<uint8_t>& data) {
    auto elfHeader = std::make_shared<ELFHeader>();
    elfHeader->isValid = false;

    if (data.size() < 64) return elfHeader;

    // Check ELF magic number
    if (data[0] != 0x7F || data[1] != 0x45 || data[2] != 0x4C || data[3] != 0x46) {
        return elfHeader;
    }

    elfHeader->isValid = true;
    elfHeader->elfClass = data[4];      // 1 = 32-bit, 2 = 64-bit
    elfHeader->dataEncoding = data[5];  // 1 = little endian, 2 = big endian
    elfHeader->type = *reinterpret_cast<const uint16_t*>(&data[16]);
    elfHeader->machine = *reinterpret_cast<const uint16_t*>(&data[18]);

    // Entry point address depends on 32/64 bit
    if (elfHeader->elfClass == 1) { // 32-bit
        elfHeader->entryPoint = *reinterpret_cast<const uint32_t*>(&data[24]);
    } else if (elfHeader->elfClass == 2) { // 64-bit
        elfHeader->entryPoint = *reinterpret_cast<const uint64_t*>(&data[24]);
    }

    return elfHeader;
}

// ==================== Packing Detection ====================

bool AdvancedScanner::detectPacking(const std::vector<uint8_t>& data, double entropy) {
    // High entropy often indicates packing/encryption
    if (entropy > entropyThreshold) {
        return true;
    }

    // Check for common packer signatures
    std::string dataStr(data.begin(), data.end());
    
    std::vector<std::string> packerSignatures = {
        "UPX", "ASPack", "PECompact", "Themida", "VMProtect"
    };

    for (const auto& sig : packerSignatures) {
        if (dataStr.find(sig) != std::string::npos) {
            return true;
        }
    }

    return false;
}

// ==================== Anti-Debug Detection ====================

bool AdvancedScanner::detectAntiDebug(const std::vector<uint8_t>& data) {
    std::string dataStr(data.begin(), data.end());
    
    std::vector<std::string> antiDebugAPIs = {
        "IsDebuggerPresent",
        "CheckRemoteDebuggerPresent",
        "NtQueryInformationProcess",
        "OutputDebugString"
    };

    for (const auto& api : antiDebugAPIs) {
        if (dataStr.find(api) != std::string::npos) {
            return true;
        }
    }

    return false;
}

// ==================== Suspicious Imports Detection ====================

bool AdvancedScanner::hasSuspiciousImports(const PEHeader& peHeader) {
    std::vector<std::string> suspiciousAPIs = {
        "VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread",
        "WinExec", "ShellExecute", "URLDownloadToFile"
    };

    for (const auto& import : peHeader.imports) {
        for (const auto& suspiciousAPI : suspiciousAPIs) {
            if (import.find(suspiciousAPI) != std::string::npos) {
                return true;
            }
        }
    }

    return false;
}

// ==================== Byte Pattern Matching ====================

bool AdvancedScanner::matchBytePattern(const std::vector<uint8_t>& data, const std::string& hexPattern) {
    auto patternBytes = ScannerUtils::hexToBytes(hexPattern);
    
    if (patternBytes.empty() || data.size() < patternBytes.size()) {
        return false;
    }

    // Simple Boyer-Moore-like search
    for (size_t i = 0; i <= data.size() - patternBytes.size(); ++i) {
        bool match = true;
        for (size_t j = 0; j < patternBytes.size(); ++j) {
            if (data[i + j] != patternBytes[j]) {
                match = false;
                break;
            }
        }
        if (match) return true;
    }

    return false;
}

// ==================== Threat Assessment ====================

ThreatLevel AdvancedScanner::assessThreatLevel(const FileAnalysis& analysis) {
    int threatScore = 0;

    // High entropy (possible packing/encryption)
    if (analysis.entropy > 7.5) threatScore += 3;
    else if (analysis.entropy > 7.0) threatScore += 2;

    // Packed executable
    if (analysis.isPacked) threatScore += 3;

    // Anti-debug techniques
    if (analysis.hasAntiDebug) threatScore += 4;

    // Suspicious imports
    if (analysis.hasSuspiciousImports) threatScore += 3;

    // Suspicious strings found
    threatScore += std::min(static_cast<int>(analysis.suspiciousStrings.size()), 5);

    // URLs or IPs embedded
    if (!analysis.urls.empty()) threatScore += 2;
    if (!analysis.ipAddresses.empty()) threatScore += 2;

    // Determine threat level based on score
    if (threatScore >= 10) return ThreatLevel::CRITICAL;
    if (threatScore >= 7) return ThreatLevel::HIGH;
    if (threatScore >= 4) return ThreatLevel::MEDIUM;
    if (threatScore >= 2) return ThreatLevel::LOW;
    
    return ThreatLevel::NONE;
}

// ==================== File Scanning ====================

FileAnalysis AdvancedScanner::scanFile(const std::string& filepath) {
    FileAnalysis analysis;
    analysis.filepath = filepath;
    analysis.threatLevel = ThreatLevel::NONE;
    analysis.isPacked = false;
    analysis.hasAntiDebug = false;
    analysis.hasSuspiciousImports = false;

    try {
        // Read file
        std::ifstream file(filepath, std::ios::binary);
        if (!file) {
            analysis.detectionReasons.push_back("Unable to open file");
            return analysis;
        }

        std::vector<uint8_t> data((std::istreambuf_iterator<char>(file)),
                                   std::istreambuf_iterator<char>());
        
        analysis.fileSize = data.size();
        
        if (data.empty()) {
            return analysis;
        }

        // Detect file type
        analysis.fileType = detectFileType(data);

        // Calculate entropy
        if (enableEntropyAnalysis) {
            analysis.entropy = calculateEntropy(data);
            analysis.isPacked = detectPacking(data, analysis.entropy);
            
            if (analysis.isPacked) {
                analysis.detectionReasons.push_back("High entropy - possible packing/encryption");
            }
        }

        // Calculate hashes
        if (enableHashCheck) {
            analysis.hashes = calculateHashes(data);
            
            // Check against known malware hashes
            if (knownMalwareHashes.count(analysis.hashes.md5) ||
                knownMalwareHashes.count(analysis.hashes.sha1) ||
                knownMalwareHashes.count(analysis.hashes.sha256)) {
                analysis.detectionReasons.push_back("Matches known malware hash");
                analysis.threatLevel = ThreatLevel::CRITICAL;
            }
        }

        // Extract strings and analyze
        if (enableStringExtraction) {
            auto strings = extractStrings(data);
            std::string allStrings;
            for (const auto& str : strings) {
                allStrings += str + " ";
                
                // Check for suspicious strings
                for (const auto& suspicious : suspiciousStrings) {
                    if (str.find(suspicious) != std::string::npos) {
                        analysis.suspiciousStrings.push_back(str);
                    }
                }
            }

            // Extract URLs, IPs, emails
            analysis.urls = extractURLs(allStrings);
            analysis.ipAddresses = extractIPAddresses(allStrings);
            analysis.emails = extractEmails(allStrings);

            if (!analysis.suspiciousStrings.empty()) {
                analysis.detectionReasons.push_back("Contains suspicious strings");
            }
            if (!analysis.urls.empty()) {
                analysis.detectionReasons.push_back("Contains embedded URLs");
            }
        }

        // Deep analysis for executables
        if (enableDeepScan) {
            if (analysis.fileType == FileType::PE_EXECUTABLE) {
                analysis.peHeader = analyzePE(data);
                if (analysis.peHeader && analysis.peHeader->isValid) {
                    analysis.hasAntiDebug = detectAntiDebug(data);
                    analysis.hasSuspiciousImports = hasSuspiciousImports(*analysis.peHeader);
                    
                    if (analysis.hasAntiDebug) {
                        analysis.detectionReasons.push_back("Contains anti-debugging techniques");
                    }
                    if (analysis.hasSuspiciousImports) {
                        analysis.detectionReasons.push_back("Contains suspicious API imports");
                    }
                }
            } else if (analysis.fileType == FileType::ELF_EXECUTABLE) {
                analysis.elfHeader = analyzeELF(data);
                if (analysis.elfHeader && analysis.elfHeader->isValid) {
                    analysis.hasAntiDebug = detectAntiDebug(data);
                    
                    if (analysis.hasAntiDebug) {
                        analysis.detectionReasons.push_back("Contains anti-debugging techniques");
                    }
                }
            }
        }

        // Check signature patterns
        for (const auto& [pattern, description] : signatures) {
            if (matchBytePattern(data, pattern)) {
                analysis.detectionReasons.push_back("Signature match: " + description);
            }
        }

        // Final threat assessment
        analysis.threatLevel = assessThreatLevel(analysis);

    } catch (const std::exception& e) {
        analysis.detectionReasons.push_back(std::string("Error during analysis: ") + e.what());
    }

    return analysis;
}

// ==================== Directory Scanning ====================

ScanResult AdvancedScanner::scanDirectory() {
    ScanResult result;
    result.timestamp = ScannerUtils::getCurrentTimestamp();
    result.totalFilesScanned = 0;
    result.threatsDetected = 0;
    
    std::cout << "[*] Starting advanced scan of: " << targetDir << std::endl;
    std::cout << "[*] Deep scan: " << (enableDeepScan ? "enabled" : "disabled") << std::endl;
    std::cout << "[*] Hash checking: " << (enableHashCheck ? "enabled" : "disabled") << std::endl;
    std::cout << "[*] Entropy analysis: " << (enableEntropyAnalysis ? "enabled" : "disabled") << std::endl;
    std::cout << std::string(60, '=') << std::endl;

    try {
        if (!fs::exists(targetDir)) {
            std::cerr << "[-] Target directory does not exist: " << targetDir << std::endl;
            return result;
        }

        for (const auto& entry : fs::recursive_directory_iterator(targetDir)) {
            if (entry.is_regular_file()) {
                result.totalFilesScanned++;
                
                std::cout << "[*] Scanning: " << entry.path().filename().string() << "..." << std::flush;
                
                FileAnalysis analysis = scanFile(entry.path().string());
                
                if (analysis.threatLevel != ThreatLevel::NONE) {
                    result.threatsDetected++;
                    result.detectedThreats.push_back(analysis);
                    result.threatsByLevel[analysis.threatLevel]++;
                    
                    std::cout << " [" << getThreatLevelString(analysis.threatLevel) << "]" << std::endl;
                    logThreat(analysis);
                } else {
                    std::cout << " [CLEAN]" << std::endl;
                }
            }
        }

    } catch (const std::exception& e) {
        std::cerr << "[-] Error during scan: " << e.what() << std::endl;
    }

    std::cout << std::string(60, '=') << std::endl;
    std::cout << "[+] Scan completed!" << std::endl;
    std::cout << "    Files scanned: " << result.totalFilesScanned << std::endl;
    std::cout << "    Threats detected: " << result.threatsDetected << std::endl;

    return result;
}

// ==================== Logging ====================

void AdvancedScanner::logThreat(const FileAnalysis& analysis) {
    std::ofstream log(logFile, std::ios::app);
    if (!log) return;

    log << "[" << ScannerUtils::getCurrentTimestamp() << "] ";
    log << "[" << getThreatLevelString(analysis.threatLevel) << "] ";
    log << analysis.filepath << std::endl;
    
    for (const auto& reason : analysis.detectionReasons) {
        log << "  - " << reason << std::endl;
    }
    
    log << "  Entropy: " << std::fixed << std::setprecision(2) << analysis.entropy << std::endl;
    log << "  File Type: " << getFileTypeString(analysis.fileType) << std::endl;
    
    if (!analysis.hashes.sha256.empty()) {
        log << "  SHA256: " << analysis.hashes.sha256 << std::endl;
    }
    
    log << std::endl;
}

// ==================== Reporting ====================

void AdvancedScanner::generateJSONReport(const ScanResult& result) {
    json report;
    
    report["timestamp"] = result.timestamp;
    report["total_files_scanned"] = result.totalFilesScanned;
    report["threats_detected"] = result.threatsDetected;
    
    // Threat statistics
    json threatStats;
    for (const auto& [level, count] : result.threatsByLevel) {
        threatStats[getThreatLevelString(level)] = count;
    }
    report["threat_statistics"] = threatStats;
    
    // Detailed threats
    json threats = json::array();
    for (const auto& threat : result.detectedThreats) {
        json t;
        t["filepath"] = threat.filepath;
        t["threat_level"] = getThreatLevelString(threat.threatLevel);
        t["file_type"] = getFileTypeString(threat.fileType);
        t["file_size"] = threat.fileSize;
        t["entropy"] = threat.entropy;
        t["is_packed"] = threat.isPacked;
        t["has_anti_debug"] = threat.hasAntiDebug;
        t["detection_reasons"] = threat.detectionReasons;
        t["suspicious_strings"] = threat.suspiciousStrings;
        t["urls"] = threat.urls;
        t["ip_addresses"] = threat.ipAddresses;
        
        if (!threat.hashes.sha256.empty()) {
            t["sha256"] = threat.hashes.sha256;
        }
        
        threats.push_back(t);
    }
    report["threats"] = threats;
    
    // Save report
    fs::create_directories(fs::path(reportFile).parent_path());
    std::ofstream outFile(reportFile);
    if (outFile) {
        outFile << report.dump(2);
        std::cout << "[+] JSON report saved to: " << reportFile << std::endl;
    }
}

void AdvancedScanner::generateTextReport(const ScanResult& result) {
    std::string textReportFile = "outputs/reports/advanced_scan_report.txt";
    std::ofstream report(textReportFile);
    
    if (!report) {
        std::cerr << "[-] Unable to create text report" << std::endl;
        return;
    }
    
    report << "========================================" << std::endl;
    report << "   THREATFUSION ADVANCED SCAN REPORT   " << std::endl;
    report << "========================================" << std::endl;
    report << "Timestamp: " << result.timestamp << std::endl;
    report << "Files Scanned: " << result.totalFilesScanned << std::endl;
    report << "Threats Detected: " << result.threatsDetected << std::endl;
    report << std::endl;
    
    if (!result.threatsByLevel.empty()) {
        report << "Threat Breakdown:" << std::endl;
        for (const auto& [level, count] : result.threatsByLevel) {
            report << "  " << getThreatLevelString(level) << ": " << count << std::endl;
        }
        report << std::endl;
    }
    
    if (!result.detectedThreats.empty()) {
        report << "Detailed Threat Analysis:" << std::endl;
        report << "========================================" << std::endl;
        
        for (const auto& threat : result.detectedThreats) {
            report << std::endl;
            report << "File: " << threat.filepath << std::endl;
            report << "Threat Level: " << getThreatLevelString(threat.threatLevel) << std::endl;
            report << "File Type: " << getFileTypeString(threat.fileType) << std::endl;
            report << "Size: " << threat.fileSize << " bytes" << std::endl;
            report << "Entropy: " << std::fixed << std::setprecision(2) << threat.entropy << std::endl;
            
            if (!threat.hashes.sha256.empty()) {
                report << "SHA256: " << threat.hashes.sha256 << std::endl;
            }
            
            report << std::endl << "Detection Reasons:" << std::endl;
            for (const auto& reason : threat.detectionReasons) {
                report << "  - " << reason << std::endl;
            }
            
            if (!threat.suspiciousStrings.empty()) {
                report << std::endl << "Suspicious Strings:" << std::endl;
                for (const auto& str : threat.suspiciousStrings) {
                    report << "  - " << str << std::endl;
                }
            }
            
            report << "----------------------------------------" << std::endl;
        }
    }
    
    std::cout << "[+] Text report saved to: " << textReportFile << std::endl;
}

// ==================== Utility Methods ====================

std::string AdvancedScanner::getThreatLevelString(ThreatLevel level) {
    switch (level) {
        case ThreatLevel::NONE: return "NONE";
        case ThreatLevel::LOW: return "LOW";
        case ThreatLevel::MEDIUM: return "MEDIUM";
        case ThreatLevel::HIGH: return "HIGH";
        case ThreatLevel::CRITICAL: return "CRITICAL";
        default: return "UNKNOWN";
    }
}

std::string AdvancedScanner::getFileTypeString(FileType type) {
    switch (type) {
        case FileType::PE_EXECUTABLE: return "PE Executable";
        case FileType::ELF_EXECUTABLE: return "ELF Executable";
        case FileType::SCRIPT: return "Script";
        case FileType::ARCHIVE: return "Archive";
        case FileType::DOCUMENT: return "Document";
        case FileType::IMAGE: return "Image";
        case FileType::BINARY: return "Binary";
        default: return "Unknown";
    }
}

void AdvancedScanner::printStatistics() {
    std::cout << "\n[*] Scan Statistics:" << std::endl;
    std::cout << "    Files scanned: " << filesScanned << std::endl;
    std::cout << "    Threats found: " << threatsFound << std::endl;
}

// ==================== Scanner Utilities ====================

namespace ScannerUtils {
    std::string bytesToHex(const std::vector<uint8_t>& bytes) {
        std::ostringstream oss;
        oss << std::hex << std::setfill('0');
        for (uint8_t byte : bytes) {
            oss << std::setw(2) << static_cast<int>(byte);
        }
        return oss.str();
    }

    std::vector<uint8_t> hexToBytes(const std::string& hex) {
        std::vector<uint8_t> bytes;
        for (size_t i = 0; i < hex.length(); i += 2) {
            std::string byteString = hex.substr(i, 2);
            uint8_t byte = static_cast<uint8_t>(std::stoi(byteString, nullptr, 16));
            bytes.push_back(byte);
        }
        return bytes;
    }

    std::string getCurrentTimestamp() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
        return ss.str();
    }

    // Simplified hash functions (use OpenSSL in production)
    std::string md5Hash(const std::vector<uint8_t>& data) {
        std::hash<std::string> hasher;
        std::string dataStr(data.begin(), data.end());
        size_t hash = hasher(dataStr);
        std::ostringstream oss;
        oss << std::hex << std::setfill('0') << std::setw(32) << hash;
        return oss.str();
    }

    std::string sha1Hash(const std::vector<uint8_t>& data) {
        std::hash<std::string> hasher;
        std::string dataStr(data.begin(), data.end());
        size_t hash = hasher(dataStr + "sha1");
        std::ostringstream oss;
        oss << std::hex << std::setfill('0') << std::setw(40) << hash;
        return oss.str();
    }

    std::string sha256Hash(const std::vector<uint8_t>& data) {
        std::hash<std::string> hasher;
        std::string dataStr(data.begin(), data.end());
        size_t hash = hasher(dataStr + "sha256");
        std::ostringstream oss;
        oss << std::hex << std::setfill('0') << std::setw(64) << hash;
        return oss.str();
    }
}
