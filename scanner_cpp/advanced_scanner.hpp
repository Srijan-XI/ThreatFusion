#ifndef ADVANCED_SCANNER_HPP
#define ADVANCED_SCANNER_HPP

#include <string>
#include <vector>
#include <map>
#include <set>
#include <cstdint>
#include <memory>

// Forward declarations
struct ScanResult;
struct FileAnalysis;
struct PEHeader;
struct ELFHeader;

// Enumeration for file types
enum class FileType {
    UNKNOWN,
    PE_EXECUTABLE,
    ELF_EXECUTABLE,
    SCRIPT,
    ARCHIVE,
    DOCUMENT,
    IMAGE,
    BINARY
};

// Enumeration for threat levels
enum class ThreatLevel {
    NONE,
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL
};

// Structure to hold PE (Portable Executable) header information
struct PEHeader {
    uint16_t machine;
    uint16_t numberOfSections;
    uint32_t timeDateStamp;
    uint32_t characteristics;
    uint16_t subsystem;
    uint64_t imageBase;
    uint32_t sizeOfImage;
    std::vector<std::string> sections;
    std::vector<std::string> imports;
    bool isValid;
};

// Structure to hold ELF (Executable and Linkable Format) header information
struct ELFHeader {
    uint8_t elfClass;      // 32-bit or 64-bit
    uint8_t dataEncoding;  // Little or big endian
    uint16_t type;         // Executable, shared object, etc.
    uint16_t machine;      // Target architecture
    uint64_t entryPoint;
    std::vector<std::string> sections;
    bool isValid;
};

// Structure to hold file hash information
struct FileHashes {
    std::string md5;
    std::string sha1;
    std::string sha256;
};

// Structure to hold file analysis results
struct FileAnalysis {
    std::string filepath;
    FileType fileType;
    uint64_t fileSize;
    double entropy;
    FileHashes hashes;
    std::vector<std::string> suspiciousStrings;
    std::vector<std::string> urls;
    std::vector<std::string> ipAddresses;
    std::vector<std::string> emails;
    ThreatLevel threatLevel;
    std::vector<std::string> detectionReasons;
    
    // Executable-specific analysis (using shared_ptr for copyability)
    std::shared_ptr<PEHeader> peHeader;
    std::shared_ptr<ELFHeader> elfHeader;
    
    bool isPacked;
    bool hasAntiDebug;
    bool hasSuspiciousImports;
};

// Structure to hold scan results
struct ScanResult {
    std::string timestamp;
    int totalFilesScanned;
    int threatsDetected;
    std::vector<FileAnalysis> detectedThreats;
    std::map<ThreatLevel, int> threatsByLevel;
};

// Main Advanced Scanner class
class AdvancedScanner {
private:
    std::string targetDir;
    std::string logFile;
    std::string reportFile;
    std::map<std::string, std::string> signatures;
    std::set<std::string> knownMalwareHashes;
    std::set<std::string> suspiciousStrings;
    
    // Configuration
    bool enableDeepScan;
    bool enableHashCheck;
    bool enableEntropyAnalysis;
    bool enableStringExtraction;
    double entropyThreshold;
    
    // Statistics
    int filesScanned;
    int threatsFound;
    
    // Private analysis methods
    FileType detectFileType(const std::vector<uint8_t>& data);
    double calculateEntropy(const std::vector<uint8_t>& data);
    FileHashes calculateHashes(const std::vector<uint8_t>& data);
    std::vector<std::string> extractStrings(const std::vector<uint8_t>& data, size_t minLength = 4);
    std::vector<std::string> extractURLs(const std::string& content);
    std::vector<std::string> extractIPAddresses(const std::string& content);
    std::vector<std::string> extractEmails(const std::string& content);
    
    // Executable analysis
    std::shared_ptr<PEHeader> analyzePE(const std::vector<uint8_t>& data);
    std::shared_ptr<ELFHeader> analyzeELF(const std::vector<uint8_t>& data);
    bool detectPacking(const std::vector<uint8_t>& data, double entropy);
    bool detectAntiDebug(const std::vector<uint8_t>& data);
    bool hasSuspiciousImports(const PEHeader& peHeader);
    
    // Threat assessment
    ThreatLevel assessThreatLevel(const FileAnalysis& analysis);
    void logThreat(const FileAnalysis& analysis);
    
    // YARA-like pattern matching
    bool matchBytePattern(const std::vector<uint8_t>& data, const std::string& hexPattern);
    
public:
    AdvancedScanner(const std::string& dir, const std::string& log);
    ~AdvancedScanner();
    
    // Configuration methods
    void setDeepScan(bool enable);
    void setHashCheck(bool enable);
    void setEntropyAnalysis(bool enable);
    void setStringExtraction(bool enable);
    void setEntropyThreshold(double threshold);
    
    // Loading methods
    void loadSignatures(const std::string& filepath);
    void loadMalwareHashes(const std::string& filepath);
    void loadSuspiciousStrings(const std::string& filepath);
    
    // Scanning methods
    ScanResult scanDirectory();
    FileAnalysis scanFile(const std::string& filepath);
    
    // Reporting methods
    void generateJSONReport(const ScanResult& result);
    void generateTextReport(const ScanResult& result);
    
    // Utility methods
    std::string getThreatLevelString(ThreatLevel level);
    std::string getFileTypeString(FileType type);
    void printStatistics();
};

// Utility functions
namespace ScannerUtils {
    std::string bytesToHex(const std::vector<uint8_t>& bytes);
    std::vector<uint8_t> hexToBytes(const std::string& hex);
    std::string getCurrentTimestamp();
    std::string md5Hash(const std::vector<uint8_t>& data);
    std::string sha1Hash(const std::vector<uint8_t>& data);
    std::string sha256Hash(const std::vector<uint8_t>& data);
}

#endif // ADVANCED_SCANNER_HPP
