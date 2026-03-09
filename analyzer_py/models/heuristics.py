#!/usr/bin/env python3
"""
Heuristic analysis patterns for threat detection
"""

import re
from typing import Dict, List, Tuple

# Threat patterns organized by severity
THREAT_PATTERNS = {
    'high': [
        r'(?i)(malware|virus|trojan|rootkit|ransomware)',
        r'(?i)(intrusion|breach|compromised|hacked)',
        r'(?i)(backdoor|shellcode|payload)',
        r'(?i)(privilege.escalation|admin.access)',
        r'(?i)(data.exfiltration|stolen.credentials)',
    ],
    'medium': [
        r'(?i)(failed.login|authentication.failed|unauthorized.access)',
        r'(?i)(suspicious.activity|anomaly.detected)',
        r'(?i)(port.scan|network.probe|reconnaissance)',
        r'(?i)(brute.force|dictionary.attack)',
        r'(?i)(injection|xss|sql)',
    ],
    'low': [
        r'(?i)(error|exception|crash|failure)',
        r'(?i)(timeout|connection.refused|unreachable)',
        r'(?i)(warning|alert|notice)',
        r'(?i)(denied|rejected|blocked)',
    ]
}

# IP address patterns (potential indicators)
IP_PATTERNS = [
    r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',  # IPv4
    r'\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b',  # IPv6
]

# Common attack signatures
ATTACK_SIGNATURES = [
    r'(?i)(cmd\.exe|powershell|bash)',
    r'(?i)(eval|exec|system|shell)',
    r'(?i)(<script|javascript:|vbscript:)',
    r'(?i)(union.*select|drop.*table|insert.*into)',
    r'(?i)(\.\.\/|\.\.\\|%2e%2e)',  # Directory traversal
]

def flag_suspicious_pattern(log_line: str) -> bool:
    """
    Check if a log line contains suspicious patterns
    
    Args:
        log_line (str): The log line to analyze
    
    Returns:
        bool: True if suspicious patterns are found
    """
    if not log_line or not isinstance(log_line, str):
        return False
    
    # Check all threat patterns
    for severity, patterns in THREAT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, log_line):
                return True
    
    # Check for attack signatures
    for pattern in ATTACK_SIGNATURES:
        if re.search(pattern, log_line):
            return True
    
    return False

def analyze_threat_level(log_line: str) -> Tuple[bool, str, List[str]]:
    """
    Analyze threat level and return detailed information
    
    Args:
        log_line (str): The log line to analyze
    
    Returns:
        Tuple[bool, str, List[str]]: (is_suspicious, severity, matched_patterns)
    """
    if not log_line or not isinstance(log_line, str):
        return False, 'none', []
    
    matched_patterns = []
    highest_severity = 'none'
    
    # Check threat patterns by severity
    severity_order = ['high', 'medium', 'low']
    
    for severity in severity_order:
        patterns = THREAT_PATTERNS.get(severity, [])
        for pattern in patterns:
            if re.search(pattern, log_line):
                matched_patterns.append(f"{severity}: {pattern}")
                if highest_severity == 'none':
                    highest_severity = severity
    
    # Check attack signatures (always high severity)
    for pattern in ATTACK_SIGNATURES:
        if re.search(pattern, log_line):
            matched_patterns.append(f"high: {pattern}")
            highest_severity = 'high'
            break
    
    is_suspicious = len(matched_patterns) > 0
    return is_suspicious, highest_severity, matched_patterns

def extract_indicators(log_line: str) -> Dict[str, List[str]]:
    """
    Extract potential indicators of compromise (IoCs) from log line
    
    Args:
        log_line (str): The log line to analyze
    
    Returns:
        Dict[str, List[str]]: Dictionary of indicator types and their values
    """
    indicators = {
        'ip_addresses': [],
        'file_paths': [],
        'urls': [],
        'hashes': []
    }
    
    if not log_line:
        return indicators
    
    # Extract IP addresses
    for pattern in IP_PATTERNS:
        matches = re.findall(pattern, log_line)
        indicators['ip_addresses'].extend(matches)
    
    # Extract file paths
    file_patterns = [
        r'[A-Za-z]:[\\\/](?:[^\\\/\s]+[\\\/])*[^\\\/\s]+',  # Windows paths
        r'\/(?:[^\/\s]+\/)*[^\/\s]+',  # Unix paths
    ]
    for pattern in file_patterns:
        matches = re.findall(pattern, log_line)
        indicators['file_paths'].extend(matches)
    
    # Extract URLs
    url_pattern = r'https?:\/\/[^\s]+'
    indicators['urls'] = re.findall(url_pattern, log_line)
    
    # Extract potential hashes (MD5, SHA1, SHA256)
    hash_patterns = [
        r'\b[a-fA-F0-9]{32}\b',  # MD5
        r'\b[a-fA-F0-9]{40}\b',  # SHA1
        r'\b[a-fA-F0-9]{64}\b',  # SHA256
    ]
    for pattern in hash_patterns:
        matches = re.findall(pattern, log_line)
        indicators['hashes'].extend(matches)
    
    return indicators
