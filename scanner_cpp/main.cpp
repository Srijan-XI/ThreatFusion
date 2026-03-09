#include <iostream>
#include <filesystem>
#include "scanner.hpp"

namespace fs = std::filesystem;

int main() {
    std::string target_dir = "data/samples";
    std::string log_file = "outputs/logs/scan.log";

    // Create directories if they don't exist
    fs::create_directories("outputs/logs");
    fs::create_directories("data/samples");

    std::cout << "[*] Starting file scan in directory: " << target_dir << std::endl;

    Scanner scanner(target_dir, log_file);
    scanner.loadSignatures("configs/rules.json");
    scanner.scanDirectory();

    std::cout << "[+] Scan completed. Results saved to: " << log_file << std::endl;
    return 0;
}
