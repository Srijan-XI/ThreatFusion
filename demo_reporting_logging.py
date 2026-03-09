#!/usr/bin/env python3
"""
ThreatFusion - Advanced Reporting and Logging Demo
Demonstrates the new logging, error handling, and reporting features
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import core modules
from core import (
    setup_logging,
    get_logger,
    get_error_handler,
    handle_errors,
    ErrorRecovery,
    ReportGenerator,
    ScannerError
)


def demo_logging():
    """Demonstrate logging capabilities"""
    print("\n" + "="*60)
    print("DEMO 1: Advanced Logging System")
    print("="*60)
    
    # Setup logger
    logger = setup_logging("ThreatFusion_Demo")
    
    logger.info("Starting ThreatFusion demo")
    logger.debug("Debug information - only visible in log files")
    logger.warning("This is a warning message")
    
    # Structured logging with extra data
    logger.log_scan_start("Advanced C++ Scanner", "data/samples")
    logger.log_scan_complete("Advanced C++ Scanner", files_scanned=150, threats_found=3)
    
    # Log threat detection
    logger.log_threat_detected(
        threat_type="Malware",
        file_path="data/samples/suspicious.exe",
        severity="HIGH",
        details={
            "hash": "abc123def456",
            "size": 102400,
            "entropy": 7.8
        }
    )
    
    # Error logging
    try:
        raise ValueError("Simulated error for demo")
    except Exception as e:
        logger.exception("An error occurred during demo")
    
    print("\n[+] Logging demo completed!")
    print("[+] Check outputs/logs/ for log files:")
    print("    - threatfusion_demo_YYYYMMDD.log (text log)")
    print("    - threatfusion_demo_YYYYMMDD.json (JSON log)")
    print("    - threatfusion_demo_errors_YYYYMMDD.log (error log)")


def demo_error_handling():
    """Demonstrate error handling capabilities"""
    print("\n" + "="*60)
    print("DEMO 2: Error Handling and Recovery")
    print("="*60)
    
    logger = get_logger()
    error_handler = get_error_handler()
    
    # Demo 1: Basic error handling with decorator
    @handle_errors(default_return=[], log_error=True)
    def risky_function():
        logger.info("Executing risky function...")
        raise ScannerError("Simulated scanner error")
    
    result = risky_function()
    print(f"[+] Risky function returned: {result}")
    
    # Demo 2: Retry mechanism
    class AttemptCounter:
        def __init__(self):
            self.count = 0
    
    counter = AttemptCounter()
    
    def flaky_network_call():
        counter.count += 1
        logger.info(f"Network call attempt #{counter.count}")
        
        if counter.count < 3:
            raise ConnectionError("Network temporarily unavailable")
        return {"status": "success", "data": "Retrieved data"}
    
    # Apply retry decorator
    retrying_call = ErrorRecovery.retry_on_failure(
        flaky_network_call,
        max_retries=3,
        delay=0.5,
        backoff=1.5
    )
    
    try:
        result = retrying_call()
        print(f"[+] Network call succeeded: {result}")
    except Exception as e:
        print(f"[-] Network call failed after retries: {e}")
    
    # Demo 3: Error summary
    summary = error_handler.get_error_summary()
    print(f"\n[+] Error Summary:")
    print(f"    Total Errors: {summary['total_errors']}")
    print(f"    Error Types: {summary['error_types']}")
    print(f"    Fatal Errors: {summary['fatal_errors']}")


def demo_reporting():
    """Demonstrate reporting capabilities"""
    print("\n" + "="*60)
    print("DEMO 3: Advanced Reporting System")
    print("="*60)
    
    logger = get_logger()
    logger.info("Generating demonstration reports")
    
    # Sample scan data
    scan_data = {
        'total_files_scanned': 250,
        'threats_detected': 5,
        'scan_duration': '3m 45s',
        'timestamp': datetime.now().isoformat(),
        'configuration': {
            'deep_scan': True,
            'hash_check': True,
            'entropy_analysis': True,
            'entropy_threshold': 7.0
        },
        'threat_statistics': {
            'CRITICAL': 1,
            'HIGH': 2,
            'MEDIUM': 1,
            'LOW': 1
        },
        'threats': [
            {
                'filepath': 'data/samples/malware.exe',
                'threat_level': 'CRITICAL',
                'file_type': 'PE Executable',
                'file_size': 204800,
                'entropy': 7.9,
                'is_packed': True,
                'has_anti_debug': True,
                'sha256': 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6',
                'detection_reasons': [
                    'High entropy detected (7.9)',
                    'Packed executable (UPX)',
                    'Anti-debugging techniques detected',
                    'Suspicious API imports: VirtualAllocEx, WriteProcessMemory',
                    'Matches known malware hash'
                ],
                'suspicious_strings': [
                    'CreateRemoteThread',
                    'VirtualAllocEx',
                    'WriteProcessMemory',
                    'IsDebuggerPresent'
                ],
                'urls': ['http://malicious-site.com/payload'],
                'ip_addresses': ['192.168.1.100', '10.0.0.5']
            },
            {
                'filepath': 'data/samples/suspicious_script.sh',
                'threat_level': 'HIGH',
                'file_type': 'Script',
                'file_size': 4096,
                'entropy': 5.2,
                'is_packed': False,
                'has_anti_debug': False,
                'sha256': 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1',
                'detection_reasons': [
                    'Contains suspicious commands',
                    'Network scanning detected',
                    'Data exfiltration patterns'
                ],
                'suspicious_strings': ['wget', 'curl', 'nmap'],
                'urls': ['http://attacker.com/upload'],
                'ip_addresses': ['10.0.0.1']
            },
            {
                'filepath': 'data/samples/adware.dll',
                'threat_level': 'HIGH',
                'file_type': 'PE Executable',
                'file_size': 81920,
                'entropy': 6.8,
                'is_packed': True,
                'has_anti_debug': False,
                'sha256': 'c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1b2',
                'detection_reasons': [
                    'Adware behavior detected',
                    'Suspicious network activity',
                    'Registry modification attempts'
                ],
                'suspicious_strings': ['RegSetValue', 'InternetOpenUrl'],
                'urls': ['http://ads-network.com'],
                'ip_addresses': []
            },
            {
                'filepath': 'data/samples/potentially_unwanted.exe',
                'threat_level': 'MEDIUM',
                'file_type': 'PE Executable',
                'file_size': 51200,
                'entropy': 6.2,
                'is_packed': False,
                'has_anti_debug': False,
                'sha256': 'd4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1b2c3',
                'detection_reasons': [
                    'Potentially unwanted program (PUP)',
                    'Bundled software detected'
                ],
                'suspicious_strings': ['InstallToolbar', 'ChangeHomepage'],
                'urls': [],
                'ip_addresses': []
            },
            {
                'filepath': 'data/samples/test_file.txt',
                'threat_level': 'LOW',
                'file_type': 'Binary',
                'file_size': 1024,
                'entropy': 4.5,
                'is_packed': False,
                'has_anti_debug': False,
                'sha256': 'e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1b2c3d4',
                'detection_reasons': [
                    'Contains suspicious strings'
                ],
                'suspicious_strings': ['cmd.exe', 'powershell'],
                'urls': [],
                'ip_addresses': []
            }
        ]
    }
    
    # Generate all reports
    print("\n[*] Generating reports in multiple formats...")
    
    report_generator = ReportGenerator()
    
    try:
        generated_reports = report_generator.generate_all_reports(scan_data)
        
        print(f"\n[+] Successfully generated {len(generated_reports)} report(s):")
        for report_type, filepath in generated_reports.items():
            print(f"    [{report_type.upper()}] {filepath}")
        
        logger.info(f"Generated {len(generated_reports)} reports", reports=list(generated_reports.keys()))
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}", exc_info=True)
        print(f"[-] Error generating reports: {e}")


def demo_integrated_workflow():
    """Demonstrate integrated workflow with all features"""
    print("\n" + "="*60)
    print("DEMO 4: Integrated Workflow")
    print("="*60)
    
    logger = get_logger()
    error_handler = get_error_handler()
    
    logger.info("Starting integrated workflow demo")
    
    # Simulate a complete scan workflow
    @handle_errors(default_return=None, log_error=True)
    def perform_scan():
        logger.info("Initializing scanner...")
        time.sleep(0.5)
        
        logger.info("Loading threat signatures...")
        time.sleep(0.3)
        
        logger.info("Scanning files...")
        time.sleep(0.5)
        
        logger.log_threat_detected(
            threat_type="Ransomware",
            file_path="data/samples/crypto_locker.exe",
            severity="CRITICAL",
            details={"encryption_detected": True}
        )
        
        logger.info("Scan completed successfully")
        
        return {
            'status': 'completed',
            'files_scanned': 100,
            'threats_found': 1
        }
    
    result = perform_scan()
    
    if result:
        print(f"\n[+] Scan completed: {result}")
        logger.info("Workflow completed successfully", result=result)
    else:
        print("\n[-] Scan failed")
        logger.error("Workflow failed")
    
    # Show final error summary
    summary = error_handler.get_error_summary()
    print(f"\n[+] Final Error Summary: {summary}")


def main():
    """Main demo function"""
    print("\n" + "="*60)
    print("ThreatFusion - Advanced Reporting & Logging Demo")
    print("="*60)
    print("\nThis demo showcases:")
    print("  1. Advanced logging with multiple outputs")
    print("  2. Robust error handling and recovery")
    print("  3. Multi-format report generation")
    print("  4. Integrated workflow example")
    
    try:
        # Run all demos
        demo_logging()
        demo_error_handling()
        demo_reporting()
        demo_integrated_workflow()
        
        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n[+] Check the following directories:")
        print("    - outputs/logs/     (log files)")
        print("    - outputs/reports/  (generated reports)")
        print("\n[+] All features are working correctly!")
        
    except Exception as e:
        print(f"\n[-] Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
