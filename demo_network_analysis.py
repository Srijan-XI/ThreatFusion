#!/usr/bin/env python3
"""
ThreatFusion Network Analysis Demo
Demonstrates network traffic analysis, protocol inspection, and threat detection
"""

import sys
import os
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from network import (
    NetworkAnalyzer,
    ProtocolAnalyzer,
    TrafficAnomalyDetector,
    GeoLocationMapper,
    ThreatIntelligence
)

from core import setup_logging, get_logger


def demo_protocol_analysis():
    """Demonstrate protocol analysis"""
    print("\n" + "="*60)
    print("DEMO 1: Protocol Analysis")
    print("="*60)
    
    logger = get_logger()
    analyzer = ProtocolAnalyzer()
    
    # Test HTTP analysis
    http_request = b"""GET /api/users?id=1' OR '1'='1 HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: */*

"""
    
    print("\n[*] Analyzing HTTP request...")
    http_result = analyzer.analyze_http(http_request)
    
    if http_result:
        print(f"[+] HTTP Analysis:")
        print(f"    Method: {http_result.get('method')}")
        print(f"    URI: {http_result.get('uri')}")
        print(f"    Suspicious: {http_result.get('suspicious')}")
        if http_result.get('flags'):
            print(f"    Flags: {', '.join(http_result['flags'])}")
    
    # Test DNS analysis
    # Simplified DNS query packet (transaction ID + flags + query for "malicious.tk")
    dns_query = b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
    dns_query += b'\x09malicious\x02tk\x00\x00\x01\x00\x01'
    
    print("\n[*] Analyzing DNS query...")
    dns_result = analyzer.analyze_dns(dns_query)
    
    if dns_result:
        print(f"[+] DNS Analysis:")
        print(f"    Queries: {dns_result.get('queries')}")
        print(f"    Suspicious: {dns_result.get('suspicious')}")
        if dns_result.get('flags'):
            print(f"    Flags: {', '.join(dns_result['flags'])}")
    
    # Test TLS analysis
    tls_handshake = b'\x16\x03\x01\x00\x05'  # TLS 1.0 handshake
    
    print("\n[*] Analyzing TLS handshake...")
    tls_result = analyzer.analyze_tls(tls_handshake)
    
    if tls_result:
        print(f"[+] TLS Analysis:")
        print(f"    Version: {tls_result.get('version')}")
        print(f"    Suspicious: {tls_result.get('suspicious')}")
        if tls_result.get('flags'):
            print(f"    Flags: {', '.join(tls_result['flags'])}")
    
    print("\n[+] Protocol analysis demo completed!")


def demo_anomaly_detection():
    """Demonstrate traffic anomaly detection"""
    print("\n" + "="*60)
    print("DEMO 2: Traffic Anomaly Detection")
    print("="*60)
    
    from network.network_analyzer import NetworkPacket
    
    detector = TrafficAnomalyDetector()
    
    print("\n[*] Simulating port scan...")
    
    # Simulate port scan (one IP scanning many ports)
    attacker_ip = "192.168.1.100"
    target_ip = "10.0.0.50"
    
    for port in range(1, 30):
        packet = NetworkPacket(
            timestamp=time.time(),
            src_ip=attacker_ip,
            dst_ip=target_ip,
            src_port=50000 + port,
            dst_port=port,
            protocol="TCP",
            packet_size=64
        )
        
        anomalies = detector.analyze_packet(packet)
        if anomalies:
            for anomaly in anomalies:
                print(f"[!] ANOMALY DETECTED: {anomaly}")
    
    print("\n[*] Simulating DDoS attack...")
    
    # Simulate DDoS (many connections from one IP)
    for i in range(110):
        packet = NetworkPacket(
            timestamp=time.time(),
            src_ip=attacker_ip,
            dst_ip=target_ip,
            src_port=50000 + i,
            dst_port=80,
            protocol="TCP",
            packet_size=64
        )
        
        anomalies = detector.analyze_packet(packet)
        if anomalies and i == 109:  # Only print on threshold breach
            for anomaly in anomalies:
                print(f"[!] ANOMALY DETECTED: {anomaly}")
    
    print("\n[*] Getting traffic statistics...")
    stats = detector.get_statistics()
    
    print(f"\n[+] Traffic Statistics:")
    print(f"    Total Packets: {stats['total_packets']}")
    print(f"    Total Bytes: {stats['total_bytes']}")
    print(f"    Unique Source IPs: {stats['unique_source_ips']}")
    print(f"    Top Talkers: {stats['top_talkers'][:3]}")
    
    print("\n[+] Anomaly detection demo completed!")


def demo_geolocation():
    """Demonstrate IP geolocation"""
    print("\n" + "="*60)
    print("DEMO 3: IP Geolocation Mapping")
    print("="*60)
    
    geo_mapper = GeoLocationMapper()
    
    test_ips = [
        "8.8.8.8",          # Google DNS (Public)
        "192.168.1.1",      # Private IP
        "1.1.1.1",          # Cloudflare DNS
        "10.0.0.1"          # Private IP
    ]
    
    print("\n[*] Looking up IP addresses...")
    
    for ip in test_ips:
        print(f"\n[*] Analyzing {ip}...")
        result = geo_mapper.lookup_ip(ip)
        
        print(f"    Type: {result.get('type')}")
        print(f"    Country: {result.get('country')}")
        print(f"    City: {result.get('city')}")
        print(f"    Organization: {result.get('org')}")
        
        if result.get('lat') and result.get('lon'):
            print(f"    Coordinates: {result['lat']}, {result['lon']}")
    
    print("\n[+] Geolocation demo completed!")


def demo_threat_intelligence():
    """Demonstrate threat intelligence integration"""
    print("\n" + "="*60)
    print("DEMO 4: Threat Intelligence Integration")
    print("="*60)
    
    # Note: This demo works without API keys but with limited functionality
    threat_intel = ThreatIntelligence()
    
    test_ips = [
        "8.8.8.8",          # Known good IP
        "192.168.1.1",      # Private IP
    ]
    
    print("\n[*] Checking IP reputation...")
    print("[!] Note: API keys required for full functionality")
    
    for ip in test_ips:
        print(f"\n[*] Checking {ip}...")
        result = threat_intel.check_ip_reputation(ip)
        
        print(f"    Is Malicious: {result['is_malicious']}")
        print(f"    Threat Score: {result['threat_score']}")
        print(f"    Sources Checked: {len(result['sources'])}")
        
        if not result['sources']:
            print("    [!] No API keys configured - limited results")
    
    print("\n[+] Threat intelligence demo completed!")


def demo_integrated_analysis():
    """Demonstrate integrated network analysis"""
    print("\n" + "="*60)
    print("DEMO 5: Integrated Network Analysis")
    print("="*60)
    
    logger = get_logger()
    analyzer = NetworkAnalyzer()
    
    print("\n[*] Network Analyzer initialized")
    print("[*] Components:")
    print("    - Protocol Analyzer")
    print("    - Anomaly Detector")
    print("    - Geolocation Mapper")
    print("    - Threat Intelligence")
    
    print("\n[!] Note: Live packet capture requires:")
    print("    1. Administrator/root privileges")
    print("    2. Scapy library installed")
    print("    3. Network interface access")
    
    print("\n[*] To capture live traffic, run:")
    print("    sudo python -c 'from network import NetworkAnalyzer; ")
    print("    analyzer = NetworkAnalyzer(); ")
    print("    analyzer.capture_traffic(duration=30, packet_count=100)'")
    
    # Simulate some analysis without actual capture
    from network.network_analyzer import NetworkPacket
    
    print("\n[*] Simulating packet analysis...")
    
    test_packets = [
        NetworkPacket(
            timestamp=time.time(),
            src_ip="192.168.1.100",
            dst_ip="8.8.8.8",
            src_port=54321,
            dst_port=53,
            protocol="UDP",
            payload=b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01',
            packet_size=45
        ),
        NetworkPacket(
            timestamp=time.time(),
            src_ip="10.0.0.50",
            dst_ip="93.184.216.34",
            src_port=50000,
            dst_port=80,
            protocol="TCP",
            payload=b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n",
            packet_size=128
        )
    ]
    
    for packet in test_packets:
        analyzer.captured_packets.append(packet)
        analyzer._analyze_packet(packet)
    
    print(f"[+] Analyzed {len(test_packets)} packets")
    
    # Generate report
    print("\n[*] Generating analysis report...")
    report_file = analyzer.generate_report()
    print(f"[+] Report saved to: {report_file}")
    
    print("\n[+] Integrated analysis demo completed!")


def main():
    """Main demo function"""
    print("\n" + "="*60)
    print("ThreatFusion Enhanced Network Analysis Demo")
    print("="*60)
    print("\nThis demo showcases:")
    print("  1. Protocol analysis (HTTP, DNS, TLS)")
    print("  2. Traffic anomaly detection")
    print("  3. IP geolocation mapping")
    print("  4. Threat intelligence integration")
    print("  5. Integrated network analysis")
    
    # Setup logging
    logger = setup_logging("NetworkAnalysis_Demo")
    logger.info("Starting network analysis demo")
    
    try:
        # Run all demos
        demo_protocol_analysis()
        demo_anomaly_detection()
        demo_geolocation()
        demo_threat_intelligence()
        demo_integrated_analysis()
        
        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n[+] Check the following directories:")
        print("    - outputs/network/  (network analysis reports)")
        print("    - outputs/logs/     (log files)")
        print("    - outputs/cache/    (geolocation cache)")
        
        print("\n[+] All network analysis features are working!")
        
        print("\n[*] Next Steps:")
        print("    1. Install scapy for packet capture: pip install scapy")
        print("    2. Get API keys for threat intelligence:")
        print("       - VirusTotal: https://www.virustotal.com/gui/join-us")
        print("       - AbuseIPDB: https://www.abuseipdb.com/register")
        print("    3. Run with elevated privileges for live capture")
        
    except Exception as e:
        print(f"\n[-] Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
