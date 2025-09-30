#!/usr/bin/env python3
"""
ThreatFusion Python Log Analyzer
Performs heuristic analysis on log files for threat detection
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from analyzer_py.models.heuristics import flag_suspicious_pattern

LOG_DIR = 'outputs/logs'
REPORTS_DIR = 'outputs/reports'

def analyze_logs():
    """Analyze all log files for suspicious patterns"""
    if not os.path.exists(LOG_DIR):
        print(f"[-] Log directory {LOG_DIR} not found")
        return []
    
    suspicious_lines = []
    total_files = 0
    total_lines = 0
    
    print(f"[*] Scanning log files in {LOG_DIR}")
    
    for filename in os.listdir(LOG_DIR):
        filepath = os.path.join(LOG_DIR, filename)
        if os.path.isfile(filepath) and filename.endswith('.log'):
            total_files += 1
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        total_lines += 1
                        if flag_suspicious_pattern(line):
                            suspicious_lines.append({
                                'filename': filename,
                                'line_number': line_num,
                                'content': line.strip(),
                                'timestamp': datetime.now().isoformat()
                            })
            except Exception as e:
                print(f"[-] Error reading {filename}: {e}")
    
    print(f"[*] Analyzed {total_files} files with {total_lines} total lines")
    return suspicious_lines

def generate_report(suspicious_lines):
    """Generate a detailed analysis report"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    report_data = {
        'analysis_timestamp': datetime.now().isoformat(),
        'total_suspicious_entries': len(suspicious_lines),
        'entries': suspicious_lines,
        'summary': {
            'files_affected': len(set(entry['filename'] for entry in suspicious_lines)),
            'threat_types': {}
        }
    }
    
    # Count threat types
    for entry in suspicious_lines:
        content_lower = entry['content'].lower()
        if 'error' in content_lower or 'failed' in content_lower:
            report_data['summary']['threat_types']['errors'] = report_data['summary']['threat_types'].get('errors', 0) + 1
        if 'unauthorized' in content_lower or 'attack' in content_lower:
            report_data['summary']['threat_types']['security_threats'] = report_data['summary']['threat_types'].get('security_threats', 0) + 1
        if 'malware' in content_lower or 'intrusion' in content_lower:
            report_data['summary']['threat_types']['malware_intrusion'] = report_data['summary']['threat_types'].get('malware_intrusion', 0) + 1
    
    # Save JSON report
    report_file = os.path.join(REPORTS_DIR, f'threat_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        print(f"[+] Detailed report saved to: {report_file}")
    except Exception as e:
        print(f"[-] Error saving report: {e}")
    
    return report_data

def main():
    """Main analysis function"""
    print("="*50)
    print("ThreatFusion Python Log Analyzer")
    print("="*50)
    
    flagged = analyze_logs()
    
    if not flagged:
        print("\n[+] No suspicious activity detected in log files")
    else:
        print(f"\n[!] Found {len(flagged)} suspicious log entries:")
        print("-" * 50)
        
        for entry in flagged:
            print(f"[{entry['filename']}:{entry['line_number']}] {entry['content']}")
        
        # Generate detailed report
        report = generate_report(flagged)
        
        print(f"\n[*] Analysis Summary:")
        print(f"    - Files affected: {report['summary']['files_affected']}")
        print(f"    - Total threats: {report['total_suspicious_entries']}")
        if report['summary']['threat_types']:
            print("    - Threat breakdown:")
            for threat_type, count in report['summary']['threat_types'].items():
                print(f"      * {threat_type.replace('_', ' ').title()}: {count}")

if __name__ == '__main__':
    main()
