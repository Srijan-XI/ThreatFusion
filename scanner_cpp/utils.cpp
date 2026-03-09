#include "scanner.hpp"
#include <iostream>
#include <fstream>
#include <filesystem>
#include <regex>
#include "json.hpp"


namespace fs = std::filesystem;
using json = nlohmann::json;

Scanner::Scanner(const std::string& dir, const std::string& log)
    : targetDir(dir), logFile(log) {}

void Scanner::loadSignatures(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file) {
        std::cerr << "[-] Unable to open signature file." << std::endl;
        return;
    }

    json j;
    file >> j;
    for (const auto& sig : j["signatures"]) {
        signatures[sig["pattern"]] = sig["description"];
    }
    std::cout << "[*] Loaded " << signatures.size() << " signatures." << std::endl;
}

void Scanner::scanDirectory() {
    std::ofstream log(logFile);
    if (!log) {
        std::cerr << "[-] Unable to create log file: " << logFile << std::endl;
        return;
    }
    
    try {
        if (!fs::exists(targetDir)) {
            std::cout << "[-] Target directory does not exist: " << targetDir << std::endl;
            log << "[-] Target directory does not exist: " << targetDir << std::endl;
            return;
        }
        
        bool found_files = false;
        for (const auto& entry : fs::recursive_directory_iterator(targetDir)) {
            if (entry.is_regular_file()) {
                found_files = true;
                scanFile(entry.path().string());
            }
        }
        
        if (!found_files) {
            std::cout << "[*] No files found in directory: " << targetDir << std::endl;
            log << "[*] No files found in directory: " << targetDir << std::endl;
        }
    } catch (const fs::filesystem_error& ex) {
        std::cerr << "[-] Filesystem error: " << ex.what() << std::endl;
        log << "[-] Filesystem error: " << ex.what() << std::endl;
    }
}

void Scanner::scanFile(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary);
    if (!file) return;

    std::ostringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();

    for (const auto& [pattern, description] : signatures) {
        std::regex hex_pattern(pattern);
        if (std::regex_search(content, hex_pattern)) {
            std::ofstream log(logFile, std::ios::app);
            log << "[!] Threat Detected in: " << filepath << " — " << description << "\n";
            std::cout << "[!] " << filepath << " -> " << description << std::endl;
        }
    }
}
