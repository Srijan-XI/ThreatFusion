#ifndef SCANNER_HPP
#define SCANNER_HPP

#include <string>
#include <vector>
#include <map>

class Scanner {
private:
    std::string targetDir;
    std::string logFile;
    std::map<std::string, std::string> signatures;

public:
    Scanner(const std::string& dir, const std::string& log);

    void loadSignatures(const std::string& filepath);
    void scanDirectory();
    void scanFile(const std::string& filepath);
};

#endif // SCANNER_HPP
