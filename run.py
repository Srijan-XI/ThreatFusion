#!/usr/bin/env python3
"""
ThreatFusion: Unified Cybersecurity Analysis Platform
Main runner script that orchestrates all components
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def check_dependencies():
    """Check if required tools are available"""
    tools = {
        'g++': ['g++', '--version'],
        'go': ['go', 'version'],
    }
    
    missing = []
    for tool, cmd in tools.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                missing.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            missing.append(tool)
    
    return missing

def compile_cpp_scanner():
    """Compile the C++ scanner"""
    print("[*] Compiling C++ scanner...")
    try:
        # Use utils.cpp instead of main.cpp for the implementation
        cmd = [
            "g++", "-std=c++17", "-o", 
            "scanner_cpp/scanner.exe" if platform.system() == "Windows" else "scanner_cpp/scanner",
            "scanner_cpp/main.cpp", "scanner_cpp/utils.cpp"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[-] C++ compilation failed: {result.stderr}")
            return False
        print("[+] C++ scanner compiled successfully")
        return True
    except Exception as e:
        print(f"[-] Error compiling C++ scanner: {e}")
        return False

def run_cpp_scanner():
    """Run the compiled C++ scanner"""
    print("[*] Running C++ scanner...")
    try:
        scanner_path = "scanner_cpp/scanner.exe" if platform.system() == "Windows" else "scanner_cpp/scanner"
        if not os.path.exists(scanner_path):
            print("[-] C++ scanner executable not found")
            return False
            
        result = subprocess.run([scanner_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[-] C++ scanner failed: {result.stderr}")
            return False
        print("[+] C++ scanner completed")
        return True
    except Exception as e:
        print(f"[-] Error running C++ scanner: {e}")
        return False

def run_go_scanner():
    """Run the Go network scanner"""
    print("[*] Running Go network scanner...")
    try:
        result = subprocess.run(["go", "run", "net_analyzer_go/netscan.go"], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode != 0:
            print(f"[-] Go scanner failed: {result.stderr}")
            return False
        print("[+] Go network scanner completed")
        return True
    except Exception as e:
        print(f"[-] Error running Go scanner: {e}")
        return False

def run_python_analyzer():
    """Run the Python log analyzer"""
    print("[*] Running Python log analyzer...")
    try:
        from analyzer_py.analyzer import analyze_logs, main
        main()
        print("[+] Python analyzer completed")
        return True
    except Exception as e:
        print(f"[-] Error running Python analyzer: {e}")
        return False

def main():
    """Main execution function"""
    print("="*60)
    print("ThreatFusion: Unified Cybersecurity Analysis Platform")
    print("="*60)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"[-] Missing dependencies: {', '.join(missing)}")
        print("[-] Please install the missing tools and try again")
        sys.exit(1)
    
    # Ensure required directories exist
    os.makedirs("outputs/logs", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)
    os.makedirs("data/samples", exist_ok=True)
    
    # Run all components
    success = True
    
    if not compile_cpp_scanner():
        success = False
    
    if success and not run_cpp_scanner():
        success = False
    
    if success and not run_go_scanner():
        success = False
    
    if success and not run_python_analyzer():
        success = False
    
    if success:
        print("\n[+] All components completed successfully")
        print("[+] Check outputs/logs/ for scan results")
    else:
        print("\n[-] Some components failed to run")
        sys.exit(1)

if __name__ == "__main__":
    main()
