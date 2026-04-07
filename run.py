#!/usr/bin/env python3
"""
ThreatFusion: Unified Cybersecurity Analysis Platform
Main runner script that orchestrates all components
"""

import subprocess
import sys
import os
import platform


SUBPROCESS_TEXT_KWARGS = {
    # Normalize subprocess output decoding across tools/platforms and avoid
    # crashes on unexpected byte sequences.
    "text": True,
    "encoding": "utf-8",
    "errors": "replace",
}

def check_dependencies():
    """Check if required tools are available"""
    # Only check external toolchain dependencies required by this orchestrator.
    tools = {
        'g++': ['g++', '--version'],
        'go': ['go', 'version'],
    }
    
    missing = []
    for tool, cmd in tools.items():
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=5, **SUBPROCESS_TEXT_KWARGS)
            if result.returncode != 0:
                missing.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            missing.append(tool)
    
    return missing

def compile_cpp_scanner():
    """Compile the C++ scanner"""
    print("[*] Compiling C++ scanner...")
    try:
        # Build platform-specific executable name while keeping shared sources.
        cmd = [
            "g++", "-std=c++17", "-o", 
            "scanner_cpp/scanner.exe" if platform.system() == "Windows" else "scanner_cpp/scanner",
            "scanner_cpp/main.cpp", "scanner_cpp/utils.cpp"
        ]
        result = subprocess.run(cmd, capture_output=True, **SUBPROCESS_TEXT_KWARGS)
        if result.returncode != 0:
            print(f"[-] C++ compilation failed: {result.stderr}")
            return False
        print("[+] C++ scanner compiled successfully")
        return True
    except Exception as e:
        print(f"[-] Error compiling C++ scanner: {e}")
        return False

def compile_advanced_scanner():
    """Compile the Advanced C++ scanner"""
    print("[*] Compiling Advanced C++ scanner...")
    try:
        # Advanced scanner enables optimization and includes local scanner headers.
        cmd = [
            "g++", "-std=c++17", "-O2", "-o",
            "scanner_cpp/advanced_scanner.exe" if platform.system() == "Windows" else "scanner_cpp/advanced_scanner",
            "scanner_cpp/advanced_main.cpp", "scanner_cpp/advanced_scanner.cpp",
            "-I", "scanner_cpp"
        ]
        result = subprocess.run(cmd, capture_output=True, **SUBPROCESS_TEXT_KWARGS)
        if result.returncode != 0:
            print(f"[-] Advanced scanner compilation failed: {result.stderr}")
            return False
        print("[+] Advanced C++ scanner compiled successfully")
        return True
    except Exception as e:
        print(f"[-] Error compiling advanced scanner: {e}")
        return False

def run_cpp_scanner():
    """Run the compiled C++ scanner"""
    print("[*] Running C++ scanner...")
    try:
        scanner_path = "scanner_cpp/scanner.exe" if platform.system() == "Windows" else "scanner_cpp/scanner"
        # Fail fast with a clear message when compilation was skipped/failed.
        if not os.path.exists(scanner_path):
            print("[-] C++ scanner executable not found")
            return False
            
        result = subprocess.run([scanner_path], capture_output=True, **SUBPROCESS_TEXT_KWARGS)
        if result.returncode != 0:
            print(f"[-] C++ scanner failed: {result.stderr}")
            return False
        print("[+] C++ scanner completed")
        return True
    except Exception as e:
        print(f"[-] Error running C++ scanner: {e}")
        return False

def run_advanced_scanner():
    """Run the Advanced C++ scanner"""
    print("[*] Running Advanced C++ scanner...")
    try:
        scanner_path = "scanner_cpp/advanced_scanner.exe" if platform.system() == "Windows" else "scanner_cpp/advanced_scanner"
        if not os.path.exists(scanner_path):
            print("[-] Advanced scanner executable not found")
            return False
        
        # Run with default settings from the scanner binary.
        result = subprocess.run([scanner_path], capture_output=True, **SUBPROCESS_TEXT_KWARGS)
        
        # Surface scanner output in the orchestrator logs for operator visibility.
        if result.stdout:
            print(result.stdout)
        
        # Return code 1 indicates "threat(s) found" in this scanner and is treated
        # as an expected analysis outcome, not a runtime failure.
        if result.returncode != 0 and result.returncode != 1:  # 1 means threats found, which is OK
            print(f"[-] Advanced scanner failed: {result.stderr}")
            return False
        
        print("[+] Advanced scanner completed")
        return True
    except Exception as e:
        print(f"[-] Error running advanced scanner: {e}")
        return False

def run_go_scanner():
    """Run the Go network scanner"""
    print("[*] Running Go network scanner...")
    try:
        # Forward optional scan configuration to the Go scanner process.
        subnet = os.getenv("THREATFUSION_SUBNET", "192.168.1.")
        ports = os.getenv("THREATFUSION_PORTS", "21,22,23,80,443,445,3306,3389,8080")
        print(f"[*] Go scan config -> subnet: {subnet} | ports: {ports}")

        child_env = os.environ.copy()
        child_env["THREATFUSION_SUBNET"] = subnet
        child_env["THREATFUSION_PORTS"] = ports

        # Execute from repository root so relative paths inside the Go toolchain
        # and project remain stable.
        result = subprocess.run(
            ["go", "run", "net_analyzer_go/netscan.go"],
            capture_output=True,
            cwd=".",
            env=child_env,
            **SUBPROCESS_TEXT_KWARGS,
        )
        if result.returncode != 0:
            print(f"[-] Go scanner failed: {result.stderr}")
            return False
        if result.stdout:
            print(result.stdout)
        print("[+] Go network scanner completed")
        return True
    except Exception as e:
        print(f"[-] Error running Go scanner: {e}")
        return False

def run_python_analyzer():
    """Run the Python log analyzer"""
    print("[*] Running Python log analyzer...")
    try:
        # Import locally so this runner can still show dependency errors cleanly.
        from analyzer_py.analyzer import main
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
    
    # Ensure output/data directories exist before scanners write artifacts.
    os.makedirs("outputs/logs", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)
    os.makedirs("data/samples", exist_ok=True)
    
    # `success` tracks critical pipeline stages; optional stages can fail
    # without terminating the entire run.
    success = True
    
    # Build scanners first so failures are detected before analysis starts.
    if not compile_cpp_scanner():
        success = False
    
    if not compile_advanced_scanner():
        print("[!] Advanced scanner compilation failed, continuing with basic scanner...")
    
    # Run basic C++ scanner
    if success and not run_cpp_scanner():
        success = False
    
    # Advanced scanner is opportunistic: run it when available but do not fail
    # the full pipeline if it errors.
    if os.path.exists("scanner_cpp/advanced_scanner.exe" if platform.system() == "Windows" else "scanner_cpp/advanced_scanner"):
        print("\n" + "="*60)
        print("Running Advanced Scanner")
        print("="*60)
        run_advanced_scanner()  # Don't fail on advanced scanner errors
    
    # Run Go scanner
    if success and not run_go_scanner():
        success = False
    
    # Run Python analyzer
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
