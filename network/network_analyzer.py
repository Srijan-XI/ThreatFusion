#!/usr/bin/env python3
"""
ThreatFusion Enhanced Network Analysis Module
Provides advanced network traffic analysis, protocol inspection, and threat detection
"""

import socket
import struct
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import threading
import queue

# Try to import optional dependencies
try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("[!] Warning: scapy not installed. Packet capture will be limited.")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[!] Warning: requests not installed. Threat intelligence features disabled.")

# Import core modules
try:
    from core import get_logger, handle_errors
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False


class NetworkPacket:
    """Represents a captured network packet"""
    
    def __init__(self, timestamp: float, src_ip: str, dst_ip: str, 
                 src_port: int, dst_port: int, protocol: str, 
                 payload: bytes = b'', packet_size: int = 0):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = protocol
        self.payload = payload
        self.packet_size = packet_size
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert packet to dictionary"""
        return {
            'timestamp': datetime.fromtimestamp(self.timestamp).isoformat(),
            'src_ip': self.src_ip,
            'dst_ip': self.dst_ip,
            'src_port': self.src_port,
            'dst_port': self.dst_port,
            'protocol': self.protocol,
            'packet_size': self.packet_size,
            'payload_preview': self.payload[:100].hex() if self.payload else ''
        }


class ProtocolAnalyzer:
    """Analyzes network protocols"""
    
    def __init__(self):
        self.http_requests = []
        self.dns_queries = []
        self.tls_connections = []
        
        if CORE_AVAILABLE:
            self.logger = get_logger()
        else:
            self.logger = None
    
    def analyze_http(self, payload: bytes) -> Optional[Dict[str, Any]]:
        """Analyze HTTP traffic"""
        try:
            payload_str = payload.decode('utf-8', errors='ignore')
            
            # Check if it's HTTP
            if not (payload_str.startswith('GET ') or payload_str.startswith('POST ') or 
                    payload_str.startswith('HTTP/')):
                return None
            
            lines = payload_str.split('\r\n')
            if not lines:
                return None
            
            # Parse request line
            request_line = lines[0]
            parts = request_line.split(' ')
            
            http_data = {
                'type': 'request' if len(parts) == 3 and parts[2].startswith('HTTP/') else 'response',
                'raw_header': request_line,
                'headers': {},
                'suspicious': False,
                'flags': []
            }
            
            if http_data['type'] == 'request':
                http_data['method'] = parts[0]
                http_data['uri'] = parts[1]
                http_data['version'] = parts[2]
            else:
                if len(parts) >= 2:
                    http_data['version'] = parts[0]
                    http_data['status_code'] = parts[1]
            
            # Parse headers
            for line in lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    http_data['headers'][key.strip()] = value.strip()
            
            # Check for suspicious patterns
            if http_data['type'] == 'request':
                uri = http_data.get('uri', '').lower()
                
                # SQL injection patterns
                if any(pattern in uri for pattern in ['union', 'select', 'drop', 'insert', '--', ';']):
                    http_data['suspicious'] = True
                    http_data['flags'].append('Possible SQL injection')
                
                # XSS patterns
                if any(pattern in uri for pattern in ['<script', 'javascript:', 'onerror=']):
                    http_data['suspicious'] = True
                    http_data['flags'].append('Possible XSS attack')
                
                # Path traversal
                if '../' in uri or '..\\' in uri:
                    http_data['suspicious'] = True
                    http_data['flags'].append('Path traversal attempt')
                
                # Command injection
                if any(pattern in uri for pattern in ['|', '&', ';', '`', '$(']):
                    http_data['suspicious'] = True
                    http_data['flags'].append('Possible command injection')
            
            self.http_requests.append(http_data)
            return http_data
            
        except Exception as e:
            if self.logger:
                self.logger.debug(f"Error analyzing HTTP: {e}")
            return None
    
    def analyze_dns(self, payload: bytes) -> Optional[Dict[str, Any]]:
        """Analyze DNS traffic"""
        try:
            if len(payload) < 12:
                return None
            
            # Parse DNS header
            transaction_id = struct.unpack('!H', payload[0:2])[0]
            flags = struct.unpack('!H', payload[2:4])[0]
            
            is_response = (flags >> 15) & 1
            opcode = (flags >> 11) & 0xF
            
            dns_data = {
                'transaction_id': transaction_id,
                'is_response': bool(is_response),
                'opcode': opcode,
                'queries': [],
                'suspicious': False,
                'flags': []
            }
            
            # Simple query name extraction (simplified)
            offset = 12
            query_name = []
            
            while offset < len(payload):
                length = payload[offset]
                if length == 0:
                    break
                if length > 63:  # Pointer or invalid
                    break
                offset += 1
                if offset + length > len(payload):
                    break
                query_name.append(payload[offset:offset+length].decode('utf-8', errors='ignore'))
                offset += length
            
            if query_name:
                domain = '.'.join(query_name)
                dns_data['queries'].append(domain)
                
                # Check for suspicious domains
                suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
                if any(domain.endswith(tld) for tld in suspicious_tlds):
                    dns_data['suspicious'] = True
                    dns_data['flags'].append('Suspicious TLD')
                
                # Check for DGA-like domains (many consonants, random-looking)
                if len(domain) > 20 and sum(c in 'aeiou' for c in domain.lower()) < len(domain) * 0.3:
                    dns_data['suspicious'] = True
                    dns_data['flags'].append('Possible DGA domain')
                
                # Check for excessive subdomain levels
                if domain.count('.') > 5:
                    dns_data['suspicious'] = True
                    dns_data['flags'].append('Excessive subdomain levels')
            
            self.dns_queries.append(dns_data)
            return dns_data
            
        except Exception as e:
            if self.logger:
                self.logger.debug(f"Error analyzing DNS: {e}")
            return None
    
    def analyze_tls(self, payload: bytes) -> Optional[Dict[str, Any]]:
        """Analyze TLS/SSL traffic"""
        try:
            if len(payload) < 5:
                return None
            
            # Check for TLS handshake
            content_type = payload[0]
            version = struct.unpack('!H', payload[1:3])[0]
            
            if content_type not in [0x14, 0x15, 0x16, 0x17]:  # TLS content types
                return None
            
            tls_data = {
                'content_type': content_type,
                'version': f"{version >> 8}.{version & 0xFF}",
                'suspicious': False,
                'flags': []
            }
            
            # Check for old/insecure TLS versions
            if version < 0x0303:  # TLS 1.2
                tls_data['suspicious'] = True
                tls_data['flags'].append('Outdated TLS version')
            
            self.tls_connections.append(tls_data)
            return tls_data
            
        except Exception as e:
            if self.logger:
                self.logger.debug(f"Error analyzing TLS: {e}")
            return None


class TrafficAnomalyDetector:
    """Detects anomalies in network traffic"""
    
    def __init__(self):
        self.connection_counts = defaultdict(int)
        self.port_scan_threshold = 20
        self.ddos_threshold = 100
        self.data_exfil_threshold = 10 * 1024 * 1024  # 10 MB
        
        self.traffic_stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'connections_per_ip': defaultdict(int),
            'ports_per_ip': defaultdict(set),
            'bytes_per_connection': defaultdict(int)
        }
        
        if CORE_AVAILABLE:
            self.logger = get_logger()
        else:
            self.logger = None
    
    def analyze_packet(self, packet: NetworkPacket) -> List[str]:
        """Analyze packet for anomalies"""
        anomalies = []
        
        self.traffic_stats['total_packets'] += 1
        self.traffic_stats['total_bytes'] += packet.packet_size
        
        # Track connections
        connection_key = f"{packet.src_ip}:{packet.src_port}->{packet.dst_ip}:{packet.dst_port}"
        self.traffic_stats['connections_per_ip'][packet.src_ip] += 1
        self.traffic_stats['ports_per_ip'][packet.src_ip].add(packet.dst_port)
        self.traffic_stats['bytes_per_connection'][connection_key] += packet.packet_size
        
        # Port scan detection
        if len(self.traffic_stats['ports_per_ip'][packet.src_ip]) > self.port_scan_threshold:
            anomalies.append(f"Port scan detected from {packet.src_ip}")
        
        # DDoS detection (many connections from single IP)
        if self.traffic_stats['connections_per_ip'][packet.src_ip] > self.ddos_threshold:
            anomalies.append(f"Possible DDoS from {packet.src_ip}")
        
        # Data exfiltration detection
        if self.traffic_stats['bytes_per_connection'][connection_key] > self.data_exfil_threshold:
            anomalies.append(f"Large data transfer detected: {connection_key}")
        
        # Suspicious ports
        suspicious_ports = [4444, 5555, 6666, 7777, 8888, 9999, 31337]
        if packet.dst_port in suspicious_ports:
            anomalies.append(f"Connection to suspicious port {packet.dst_port}")
        
        return anomalies
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get traffic statistics"""
        return {
            'total_packets': self.traffic_stats['total_packets'],
            'total_bytes': self.traffic_stats['total_bytes'],
            'unique_source_ips': len(self.traffic_stats['connections_per_ip']),
            'top_talkers': sorted(
                self.traffic_stats['connections_per_ip'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


class GeoLocationMapper:
    """Maps IP addresses to geographic locations"""
    
    def __init__(self, cache_file: str = "outputs/cache/geo_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache = self._load_cache()
        
        if CORE_AVAILABLE:
            self.logger = get_logger()
        else:
            self.logger = None
    
    def _load_cache(self) -> Dict[str, Dict[str, Any]]:
        """Load geolocation cache"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save geolocation cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to save geo cache: {e}")
    
    def lookup_ip(self, ip_address: str) -> Dict[str, Any]:
        """Lookup IP geolocation"""
        # Check cache first
        if ip_address in self.cache:
            return self.cache[ip_address]
        
        # Skip private IPs
        if self._is_private_ip(ip_address):
            result = {
                'ip': ip_address,
                'type': 'private',
                'country': 'N/A',
                'city': 'N/A',
                'org': 'Private Network'
            }
            self.cache[ip_address] = result
            return result
        
        # Use free IP geolocation API
        if REQUESTS_AVAILABLE:
            try:
                response = requests.get(
                    f"http://ip-api.com/json/{ip_address}",
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = {
                        'ip': ip_address,
                        'type': 'public',
                        'country': data.get('country', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'isp': data.get('isp', 'Unknown'),
                        'org': data.get('org', 'Unknown'),
                        'lat': data.get('lat'),
                        'lon': data.get('lon')
                    }
                    self.cache[ip_address] = result
                    self._save_cache()
                    return result
            except Exception as e:
                if self.logger:
                    self.logger.debug(f"Geolocation lookup failed for {ip_address}: {e}")
        
        # Fallback
        result = {
            'ip': ip_address,
            'type': 'public',
            'country': 'Unknown',
            'city': 'Unknown',
            'org': 'Unknown'
        }
        return result
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private"""
        try:
            parts = [int(p) for p in ip.split('.')]
            
            # 10.0.0.0/8
            if parts[0] == 10:
                return True
            
            # 172.16.0.0/12
            if parts[0] == 172 and 16 <= parts[1] <= 31:
                return True
            
            # 192.168.0.0/16
            if parts[0] == 192 and parts[1] == 168:
                return True
            
            # 127.0.0.0/8 (loopback)
            if parts[0] == 127:
                return True
            
            return False
        except:
            return False


class ThreatIntelligence:
    """Integrates with threat intelligence services"""
    
    def __init__(self, virustotal_api_key: Optional[str] = None,
                 abuseipdb_api_key: Optional[str] = None):
        self.vt_api_key = virustotal_api_key
        self.abuseipdb_api_key = abuseipdb_api_key
        
        if CORE_AVAILABLE:
            self.logger = get_logger()
        else:
            self.logger = None
    
    def check_ip_reputation(self, ip_address: str) -> Dict[str, Any]:
        """Check IP reputation across multiple sources"""
        result = {
            'ip': ip_address,
            'is_malicious': False,
            'threat_score': 0,
            'sources': []
        }
        
        # Check AbuseIPDB
        if self.abuseipdb_api_key and REQUESTS_AVAILABLE:
            abuse_result = self._check_abuseipdb(ip_address)
            if abuse_result:
                result['sources'].append(abuse_result)
                if abuse_result.get('abuse_confidence_score', 0) > 50:
                    result['is_malicious'] = True
                    result['threat_score'] += abuse_result['abuse_confidence_score']
        
        # Check VirusTotal
        if self.vt_api_key and REQUESTS_AVAILABLE:
            vt_result = self._check_virustotal_ip(ip_address)
            if vt_result:
                result['sources'].append(vt_result)
                if vt_result.get('malicious_count', 0) > 0:
                    result['is_malicious'] = True
                    result['threat_score'] += vt_result['malicious_count'] * 10
        
        return result
    
    def _check_abuseipdb(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Check IP against AbuseIPDB"""
        try:
            headers = {
                'Key': self.abuseipdb_api_key,
                'Accept': 'application/json'
            }
            
            response = requests.get(
                f'https://api.abuseipdb.com/api/v2/check',
                params={'ipAddress': ip_address, 'maxAgeInDays': 90},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()['data']
                return {
                    'source': 'AbuseIPDB',
                    'abuse_confidence_score': data.get('abuseConfidenceScore', 0),
                    'total_reports': data.get('totalReports', 0),
                    'is_whitelisted': data.get('isWhitelisted', False)
                }
        except Exception as e:
            if self.logger:
                self.logger.debug(f"AbuseIPDB check failed: {e}")
        
        return None
    
    def _check_virustotal_ip(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Check IP against VirusTotal"""
        try:
            headers = {'x-apikey': self.vt_api_key}
            
            response = requests.get(
                f'https://www.virustotal.com/api/v3/ip_addresses/{ip_address}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()['data']['attributes']
                stats = data.get('last_analysis_stats', {})
                
                return {
                    'source': 'VirusTotal',
                    'malicious_count': stats.get('malicious', 0),
                    'suspicious_count': stats.get('suspicious', 0),
                    'harmless_count': stats.get('harmless', 0),
                    'reputation': data.get('reputation', 0)
                }
        except Exception as e:
            if self.logger:
                self.logger.debug(f"VirusTotal check failed: {e}")
        
        return None


class NetworkAnalyzer:
    """Main network analysis class"""
    
    def __init__(self, output_dir: str = "outputs/network"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.protocol_analyzer = ProtocolAnalyzer()
        self.anomaly_detector = TrafficAnomalyDetector()
        self.geo_mapper = GeoLocationMapper()
        self.threat_intel = ThreatIntelligence()
        
        self.captured_packets = []
        self.analysis_results = []
        
        if CORE_AVAILABLE:
            self.logger = get_logger()
        else:
            self.logger = None
    
    @handle_errors(default_return=[], log_error=True) if CORE_AVAILABLE else lambda f: f
    def capture_traffic(self, interface: str = None, duration: int = 60, 
                       packet_count: int = 100) -> List[NetworkPacket]:
        """Capture network traffic"""
        if not SCAPY_AVAILABLE:
            print("[!] Scapy not available. Using basic socket capture.")
            return self._basic_capture(duration, packet_count)
        
        if self.logger:
            self.logger.info(f"Starting packet capture for {duration}s")
        
        packets = []
        
        def packet_handler(pkt):
            try:
                if pkt.haslayer(scapy.IP):
                    ip_layer = pkt[scapy.IP]
                    
                    src_port = 0
                    dst_port = 0
                    protocol = 'IP'
                    payload = b''
                    
                    if pkt.haslayer(scapy.TCP):
                        tcp_layer = pkt[scapy.TCP]
                        src_port = tcp_layer.sport
                        dst_port = tcp_layer.dport
                        protocol = 'TCP'
                        payload = bytes(tcp_layer.payload) if tcp_layer.payload else b''
                    elif pkt.haslayer(scapy.UDP):
                        udp_layer = pkt[scapy.UDP]
                        src_port = udp_layer.sport
                        dst_port = udp_layer.dport
                        protocol = 'UDP'
                        payload = bytes(udp_layer.payload) if udp_layer.payload else b''
                    
                    packet = NetworkPacket(
                        timestamp=time.time(),
                        src_ip=ip_layer.src,
                        dst_ip=ip_layer.dst,
                        src_port=src_port,
                        dst_port=dst_port,
                        protocol=protocol,
                        payload=payload,
                        packet_size=len(pkt)
                    )
                    
                    packets.append(packet)
                    self.captured_packets.append(packet)
                    
                    # Analyze packet
                    self._analyze_packet(packet)
                    
            except Exception as e:
                if self.logger:
                    self.logger.debug(f"Error processing packet: {e}")
        
        # Capture packets
        scapy.sniff(iface=interface, prn=packet_handler, timeout=duration, count=packet_count)
        
        if self.logger:
            self.logger.info(f"Captured {len(packets)} packets")
        
        return packets
    
    def _basic_capture(self, duration: int, packet_count: int) -> List[NetworkPacket]:
        """Basic packet capture without scapy"""
        print("[*] Basic capture mode - limited functionality")
        # Placeholder for basic capture
        return []
    
    def _analyze_packet(self, packet: NetworkPacket):
        """Analyze a single packet"""
        analysis = {
            'packet': packet.to_dict(),
            'protocol_analysis': {},
            'anomalies': [],
            'geolocation': {}
        }
        
        # Protocol analysis
        if packet.protocol == 'TCP':
            if packet.dst_port == 80 or packet.src_port == 80:
                http_analysis = self.protocol_analyzer.analyze_http(packet.payload)
                if http_analysis:
                    analysis['protocol_analysis']['http'] = http_analysis
            
            elif packet.dst_port == 443 or packet.src_port == 443:
                tls_analysis = self.protocol_analyzer.analyze_tls(packet.payload)
                if tls_analysis:
                    analysis['protocol_analysis']['tls'] = tls_analysis
        
        elif packet.protocol == 'UDP':
            if packet.dst_port == 53 or packet.src_port == 53:
                dns_analysis = self.protocol_analyzer.analyze_dns(packet.payload)
                if dns_analysis:
                    analysis['protocol_analysis']['dns'] = dns_analysis
        
        # Anomaly detection
        anomalies = self.anomaly_detector.analyze_packet(packet)
        if anomalies:
            analysis['anomalies'] = anomalies
        
        # Geolocation
        if packet.dst_ip:
            analysis['geolocation'] = self.geo_mapper.lookup_ip(packet.dst_ip)
        
        self.analysis_results.append(analysis)
    
    def generate_report(self) -> str:
        """Generate network analysis report"""
        report_file = self.output_dir / f"network_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_packets': len(self.captured_packets),
                'protocols': self._count_protocols(),
                'unique_ips': self._count_unique_ips(),
                'suspicious_activities': self._count_suspicious()
            },
            'statistics': self.anomaly_detector.get_statistics(),
            'analysis_results': self.analysis_results[:100]  # Limit to first 100
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        if self.logger:
            self.logger.info(f"Network analysis report saved to {report_file}")
        
        return str(report_file)
    
    def _count_protocols(self) -> Dict[str, int]:
        """Count packets by protocol"""
        counts = defaultdict(int)
        for packet in self.captured_packets:
            counts[packet.protocol] += 1
        return dict(counts)
    
    def _count_unique_ips(self) -> Dict[str, int]:
        """Count unique IP addresses"""
        src_ips = set(p.src_ip for p in self.captured_packets)
        dst_ips = set(p.dst_ip for p in self.captured_packets)
        return {
            'source': len(src_ips),
            'destination': len(dst_ips),
            'total': len(src_ips | dst_ips)
        }
    
    def _count_suspicious(self) -> int:
        """Count suspicious activities"""
        count = 0
        for result in self.analysis_results:
            if result.get('anomalies'):
                count += 1
            
            proto_analysis = result.get('protocol_analysis', {})
            for proto_data in proto_analysis.values():
                if isinstance(proto_data, dict) and proto_data.get('suspicious'):
                    count += 1
        
        return count


if __name__ == "__main__":
    print("ThreatFusion Enhanced Network Analysis Module")
    print("=" * 60)
    
    analyzer = NetworkAnalyzer()
    
    print("\n[*] This module provides:")
    print("  - Network packet capture and analysis")
    print("  - Protocol inspection (HTTP, DNS, TLS)")
    print("  - Traffic anomaly detection")
    print("  - IP geolocation mapping")
    print("  - Threat intelligence integration")
    
    print("\n[!] Note: Packet capture requires elevated privileges")
    print("[!] Install scapy for full functionality: pip install scapy")
    
    print("\n[+] Module loaded successfully!")
