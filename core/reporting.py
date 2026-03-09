#!/usr/bin/env python3
"""
ThreatFusion Advanced Reporting System
Generates comprehensive reports in multiple formats: PDF, HTML, Excel, CSV
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import csv

# Try to import optional dependencies
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("[!] Warning: fpdf not installed. PDF reports will be unavailable.")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("[!] Warning: pandas not installed. Excel/CSV reports will be limited.")

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[!] Warning: matplotlib not installed. Charts will be unavailable.")


class ThreatFusionReport:
    """Base class for ThreatFusion reports"""
    
    def __init__(self, report_dir: str = "outputs/reports"):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now()
        
    def _generate_filename(self, prefix: str, extension: str) -> Path:
        """Generate timestamped filename"""
        timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S")
        return self.report_dir / f"{prefix}_{timestamp_str}.{extension}"


class PDFReport(ThreatFusionReport):
    """Generate PDF reports"""
    
    def __init__(self, report_dir: str = "outputs/reports"):
        super().__init__(report_dir)
        if not PDF_AVAILABLE:
            raise ImportError("fpdf is required for PDF reports. Install with: pip install fpdf")
    
    def generate_executive_summary(self, scan_data: Dict[str, Any]) -> str:
        """Generate executive summary PDF report"""
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 20, 'ThreatFusion Security Report', 0, 1, 'C')
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(0, 10, f'Executive Summary - {self.timestamp.strftime("%B %d, %Y")}', 0, 1, 'C')
        pdf.ln(10)
        
        # Summary Section
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Scan Summary', 0, 1)
        pdf.set_font('Arial', '', 12)
        
        summary_data = [
            ('Scan Date', self.timestamp.strftime("%Y-%m-%d %H:%M:%S")),
            ('Total Files Scanned', str(scan_data.get('total_files_scanned', 0))),
            ('Threats Detected', str(scan_data.get('threats_detected', 0))),
            ('Scan Duration', scan_data.get('scan_duration', 'N/A')),
        ]
        
        for label, value in summary_data:
            pdf.cell(80, 8, f'{label}:', 0, 0)
            pdf.cell(0, 8, value, 0, 1)
        
        pdf.ln(5)
        
        # Threat Breakdown
        if 'threat_statistics' in scan_data:
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Threat Breakdown by Severity', 0, 1)
            pdf.set_font('Arial', '', 12)
            
            for level, count in scan_data['threat_statistics'].items():
                pdf.cell(80, 8, f'{level}:', 0, 0)
                pdf.cell(0, 8, str(count), 0, 1)
            
            pdf.ln(5)
        
        # Detailed Threats
        if 'threats' in scan_data and scan_data['threats']:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Detected Threats', 0, 1)
            
            for i, threat in enumerate(scan_data['threats'][:20], 1):  # Limit to first 20
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 8, f'Threat #{i}', 0, 1)
                pdf.set_font('Arial', '', 10)
                
                pdf.cell(60, 6, 'File:', 0, 0)
                pdf.multi_cell(0, 6, threat.get('filepath', 'Unknown'))
                
                pdf.cell(60, 6, 'Threat Level:', 0, 0)
                pdf.cell(0, 6, threat.get('threat_level', 'Unknown'), 0, 1)
                
                pdf.cell(60, 6, 'File Type:', 0, 0)
                pdf.cell(0, 6, threat.get('file_type', 'Unknown'), 0, 1)
                
                if 'detection_reasons' in threat and threat['detection_reasons']:
                    pdf.cell(60, 6, 'Detection Reasons:', 0, 1)
                    for reason in threat['detection_reasons'][:3]:  # Limit to 3 reasons
                        pdf.cell(10, 6, '', 0, 0)
                        pdf.multi_cell(0, 6, f'- {reason}')
                
                pdf.ln(3)
        
        # Recommendations
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Recommendations', 0, 1)
        pdf.set_font('Arial', '', 12)
        
        recommendations = self._generate_recommendations(scan_data)
        for rec in recommendations:
            pdf.multi_cell(0, 6, f'• {rec}')
            pdf.ln(2)
        
        # Save PDF
        output_file = self._generate_filename('executive_summary', 'pdf')
        pdf.output(str(output_file))
        
        return str(output_file)
    
    def generate_technical_report(self, scan_data: Dict[str, Any]) -> str:
        """Generate detailed technical PDF report"""
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 20, 'ThreatFusion Technical Report', 0, 1, 'C')
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(0, 10, f'Detailed Analysis - {self.timestamp.strftime("%B %d, %Y")}', 0, 1, 'C')
        pdf.ln(10)
        
        # Technical Details
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Scan Configuration', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        config_data = scan_data.get('configuration', {})
        for key, value in config_data.items():
            pdf.cell(80, 6, f'{key}:', 0, 0)
            pdf.cell(0, 6, str(value), 0, 1)
        
        pdf.ln(5)
        
        # All Threats with Full Details
        if 'threats' in scan_data and scan_data['threats']:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'Complete Threat Analysis', 0, 1)
            
            for i, threat in enumerate(scan_data['threats'], 1):
                if i > 1 and i % 3 == 0:  # New page every 3 threats
                    pdf.add_page()
                
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 7, f'Threat #{i}: {threat.get("filepath", "Unknown")}', 0, 1)
                pdf.set_font('Arial', '', 9)
                
                # All available details
                details = [
                    ('Threat Level', threat.get('threat_level', 'N/A')),
                    ('File Type', threat.get('file_type', 'N/A')),
                    ('File Size', f'{threat.get("file_size", 0)} bytes'),
                    ('Entropy', f'{threat.get("entropy", 0):.2f}'),
                    ('Is Packed', str(threat.get('is_packed', False))),
                    ('Has Anti-Debug', str(threat.get('has_anti_debug', False))),
                ]
                
                for label, value in details:
                    pdf.cell(50, 5, f'{label}:', 0, 0)
                    pdf.cell(0, 5, str(value), 0, 1)
                
                # Hashes
                if 'sha256' in threat:
                    pdf.cell(50, 5, 'SHA256:', 0, 0)
                    pdf.set_font('Courier', '', 8)
                    pdf.cell(0, 5, threat['sha256'], 0, 1)
                    pdf.set_font('Arial', '', 9)
                
                # Detection reasons
                if 'detection_reasons' in threat and threat['detection_reasons']:
                    pdf.cell(0, 5, 'Detection Reasons:', 0, 1)
                    for reason in threat['detection_reasons']:
                        pdf.cell(5, 5, '', 0, 0)
                        pdf.multi_cell(0, 5, f'• {reason}')
                
                # Suspicious strings
                if 'suspicious_strings' in threat and threat['suspicious_strings']:
                    pdf.cell(0, 5, 'Suspicious Strings:', 0, 1)
                    for string in threat['suspicious_strings'][:5]:
                        pdf.cell(5, 5, '', 0, 0)
                        pdf.multi_cell(0, 5, f'• {string}')
                
                # URLs and IPs
                if 'urls' in threat and threat['urls']:
                    pdf.cell(0, 5, f'URLs Found: {len(threat["urls"])}', 0, 1)
                
                if 'ip_addresses' in threat and threat['ip_addresses']:
                    pdf.cell(0, 5, f'IP Addresses Found: {len(threat["ip_addresses"])}', 0, 1)
                
                pdf.ln(3)
        
        # Save PDF
        output_file = self._generate_filename('technical_report', 'pdf')
        pdf.output(str(output_file))
        
        return str(output_file)
    
    def _generate_recommendations(self, scan_data: Dict[str, Any]) -> List[str]:
        """Generate security recommendations based on scan results"""
        recommendations = []
        
        threats_count = scan_data.get('threats_detected', 0)
        
        if threats_count == 0:
            recommendations.append("No threats detected. Continue regular security monitoring.")
            recommendations.append("Maintain up-to-date antivirus and security software.")
        else:
            recommendations.append(f"URGENT: {threats_count} threat(s) detected. Immediate action required.")
            recommendations.append("Quarantine or delete all detected threats immediately.")
            recommendations.append("Run a full system scan with updated antivirus software.")
            recommendations.append("Review system logs for any suspicious activity.")
            recommendations.append("Consider changing passwords for sensitive accounts.")
        
        # Specific recommendations based on threat types
        if 'threat_statistics' in scan_data:
            stats = scan_data['threat_statistics']
            
            if stats.get('CRITICAL', 0) > 0 or stats.get('HIGH', 0) > 0:
                recommendations.append("High-severity threats detected. Consider professional security audit.")
                recommendations.append("Disconnect affected systems from network until threats are removed.")
            
            if stats.get('MEDIUM', 0) > 0:
                recommendations.append("Monitor systems closely for any unusual behavior.")
        
        recommendations.append("Implement regular automated security scans.")
        recommendations.append("Keep all software and operating systems up to date.")
        recommendations.append("Enable firewall and intrusion detection systems.")
        
        return recommendations


class HTMLReport(ThreatFusionReport):
    """Generate HTML reports with interactive elements"""
    
    def generate_dashboard(self, scan_data: Dict[str, Any]) -> str:
        """Generate interactive HTML dashboard"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ThreatFusion Security Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card h3 {{
            color: #2a5298;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #1e3c72;
        }}
        
        .threat-level {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .threat-level.critical {{
            background: #e74c3c;
            color: white;
        }}
        
        .threat-level.high {{
            background: #e67e22;
            color: white;
        }}
        
        .threat-level.medium {{
            background: #f39c12;
            color: white;
        }}
        
        .threat-level.low {{
            background: #3498db;
            color: white;
        }}
        
        .threat-level.none {{
            background: #2ecc71;
            color: white;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #1e3c72;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #2a5298;
        }}
        
        .threat-list {{
            list-style: none;
        }}
        
        .threat-item {{
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #2a5298;
        }}
        
        .threat-item h4 {{
            color: #1e3c72;
            margin-bottom: 10px;
        }}
        
        .threat-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
            font-size: 0.9em;
        }}
        
        .threat-details div {{
            padding: 8px;
            background: white;
            border-radius: 5px;
        }}
        
        .threat-details strong {{
            color: #2a5298;
        }}
        
        .detection-reasons {{
            margin-top: 15px;
        }}
        
        .detection-reasons ul {{
            margin-left: 20px;
            margin-top: 10px;
        }}
        
        .detection-reasons li {{
            margin-bottom: 5px;
            color: #555;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .chart-container {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ ThreatFusion Security Report</h1>
            <p>Generated on {self.timestamp.strftime("%B %d, %Y at %H:%M:%S")}</p>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Files Scanned</h3>
                    <div class="value">{scan_data.get('total_files_scanned', 0)}</div>
                </div>
                <div class="stat-card">
                    <h3>Threats Detected</h3>
                    <div class="value">{scan_data.get('threats_detected', 0)}</div>
                </div>
                <div class="stat-card">
                    <h3>Scan Duration</h3>
                    <div class="value">{scan_data.get('scan_duration', 'N/A')}</div>
                </div>
                <div class="stat-card">
                    <h3>Scan Date</h3>
                    <div class="value" style="font-size: 1.2em;">{self.timestamp.strftime("%Y-%m-%d")}</div>
                </div>
            </div>
"""
        
        # Threat statistics
        if 'threat_statistics' in scan_data and scan_data['threat_statistics']:
            html_content += """
            <div class="section">
                <h2>📊 Threat Breakdown by Severity</h2>
                <div class="stats-grid">
"""
            for level, count in scan_data['threat_statistics'].items():
                html_content += f"""
                    <div class="stat-card">
                        <h3>{level}</h3>
                        <div class="value">{count}</div>
                    </div>
"""
            html_content += """
                </div>
            </div>
"""
        
        # Detected threats
        if 'threats' in scan_data and scan_data['threats']:
            html_content += """
            <div class="section">
                <h2>🚨 Detected Threats</h2>
                <ul class="threat-list">
"""
            for i, threat in enumerate(scan_data['threats'], 1):
                threat_level = threat.get('threat_level', 'UNKNOWN').lower()
                html_content += f"""
                    <li class="threat-item">
                        <h4>Threat #{i}: {threat.get('filepath', 'Unknown')}</h4>
                        <span class="threat-level {threat_level}">{threat.get('threat_level', 'UNKNOWN')}</span>
                        
                        <div class="threat-details">
                            <div><strong>File Type:</strong> {threat.get('file_type', 'Unknown')}</div>
                            <div><strong>File Size:</strong> {threat.get('file_size', 0)} bytes</div>
                            <div><strong>Entropy:</strong> {threat.get('entropy', 0):.2f}</div>
                            <div><strong>Packed:</strong> {threat.get('is_packed', False)}</div>
                        </div>
"""
                
                if 'detection_reasons' in threat and threat['detection_reasons']:
                    html_content += """
                        <div class="detection-reasons">
                            <strong>Detection Reasons:</strong>
                            <ul>
"""
                    for reason in threat['detection_reasons']:
                        html_content += f"<li>{reason}</li>\n"
                    html_content += """
                            </ul>
                        </div>
"""
                
                html_content += """
                    </li>
"""
            html_content += """
                </ul>
            </div>
"""
        else:
            html_content += """
            <div class="section">
                <h2>✅ No Threats Detected</h2>
                <p style="font-size: 1.2em; color: #2ecc71;">Your system appears to be clean!</p>
            </div>
"""
        
        html_content += f"""
        </div>
        
        <div class="footer">
            <p>ThreatFusion Advanced Cybersecurity Analysis Platform</p>
            <p>Report generated by ThreatFusion v2.0</p>
        </div>
    </div>
</body>
</html>
"""
        
        output_file = self._generate_filename('dashboard', 'html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_file)


class ExcelReport(ThreatFusionReport):
    """Generate Excel reports"""
    
    def __init__(self, report_dir: str = "outputs/reports"):
        super().__init__(report_dir)
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for Excel reports. Install with: pip install pandas openpyxl")
    
    def generate_detailed_report(self, scan_data: Dict[str, Any]) -> str:
        """Generate detailed Excel report with multiple sheets"""
        
        output_file = self._generate_filename('detailed_report', 'xlsx')
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = {
                'Metric': [
                    'Scan Date',
                    'Total Files Scanned',
                    'Threats Detected',
                    'Scan Duration'
                ],
                'Value': [
                    self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    scan_data.get('total_files_scanned', 0),
                    scan_data.get('threats_detected', 0),
                    scan_data.get('scan_duration', 'N/A')
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Threat statistics sheet
            if 'threat_statistics' in scan_data:
                stats_data = {
                    'Threat Level': list(scan_data['threat_statistics'].keys()),
                    'Count': list(scan_data['threat_statistics'].values())
                }
                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Threat Statistics', index=False)
            
            # Detailed threats sheet
            if 'threats' in scan_data and scan_data['threats']:
                threats_list = []
                for threat in scan_data['threats']:
                    threats_list.append({
                        'File Path': threat.get('filepath', ''),
                        'Threat Level': threat.get('threat_level', ''),
                        'File Type': threat.get('file_type', ''),
                        'File Size': threat.get('file_size', 0),
                        'Entropy': threat.get('entropy', 0),
                        'Is Packed': threat.get('is_packed', False),
                        'Has Anti-Debug': threat.get('has_anti_debug', False),
                        'SHA256': threat.get('sha256', ''),
                        'Detection Reasons': '; '.join(threat.get('detection_reasons', []))
                    })
                
                df_threats = pd.DataFrame(threats_list)
                df_threats.to_excel(writer, sheet_name='Detected Threats', index=False)
        
        return str(output_file)


class CSVReport(ThreatFusionReport):
    """Generate CSV reports"""
    
    def generate_threat_list(self, scan_data: Dict[str, Any]) -> str:
        """Generate CSV file with threat list"""
        
        output_file = self._generate_filename('threat_list', 'csv')
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'File Path', 'Threat Level', 'File Type', 'File Size',
                'Entropy', 'Is Packed', 'Has Anti-Debug', 'SHA256', 'Detection Reasons'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            if 'threats' in scan_data:
                for threat in scan_data['threats']:
                    writer.writerow({
                        'File Path': threat.get('filepath', ''),
                        'Threat Level': threat.get('threat_level', ''),
                        'File Type': threat.get('file_type', ''),
                        'File Size': threat.get('file_size', 0),
                        'Entropy': f"{threat.get('entropy', 0):.2f}",
                        'Is Packed': threat.get('is_packed', False),
                        'Has Anti-Debug': threat.get('has_anti_debug', False),
                        'SHA256': threat.get('sha256', ''),
                        'Detection Reasons': '; '.join(threat.get('detection_reasons', []))
                    })
        
        return str(output_file)


class ReportGenerator:
    """Main report generator class"""
    
    def __init__(self, report_dir: str = "outputs/reports"):
        self.report_dir = report_dir
        
    def generate_all_reports(self, scan_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate all available report formats"""
        
        generated_reports = {}
        
        # HTML Report (always available)
        try:
            html_gen = HTMLReport(self.report_dir)
            html_file = html_gen.generate_dashboard(scan_data)
            generated_reports['html'] = html_file
            print(f"[+] HTML report generated: {html_file}")
        except Exception as e:
            print(f"[-] Error generating HTML report: {e}")
        
        # PDF Reports
        if PDF_AVAILABLE:
            try:
                pdf_gen = PDFReport(self.report_dir)
                exec_pdf = pdf_gen.generate_executive_summary(scan_data)
                tech_pdf = pdf_gen.generate_technical_report(scan_data)
                generated_reports['pdf_executive'] = exec_pdf
                generated_reports['pdf_technical'] = tech_pdf
                print(f"[+] PDF Executive Summary: {exec_pdf}")
                print(f"[+] PDF Technical Report: {tech_pdf}")
            except Exception as e:
                print(f"[-] Error generating PDF reports: {e}")
        
        # Excel Report
        if PANDAS_AVAILABLE:
            try:
                excel_gen = ExcelReport(self.report_dir)
                excel_file = excel_gen.generate_detailed_report(scan_data)
                generated_reports['excel'] = excel_file
                print(f"[+] Excel report generated: {excel_file}")
            except Exception as e:
                print(f"[-] Error generating Excel report: {e}")
        
        # CSV Report
        try:
            csv_gen = CSVReport(self.report_dir)
            csv_file = csv_gen.generate_threat_list(scan_data)
            generated_reports['csv'] = csv_file
            print(f"[+] CSV report generated: {csv_file}")
        except Exception as e:
            print(f"[-] Error generating CSV report: {e}")
        
        return generated_reports


if __name__ == "__main__":
    # Test report generation
    test_data = {
        'total_files_scanned': 150,
        'threats_detected': 3,
        'scan_duration': '2m 34s',
        'threat_statistics': {
            'CRITICAL': 1,
            'HIGH': 1,
            'MEDIUM': 1
        },
        'threats': [
            {
                'filepath': '/path/to/malware.exe',
                'threat_level': 'CRITICAL',
                'file_type': 'PE Executable',
                'file_size': 102400,
                'entropy': 7.8,
                'is_packed': True,
                'has_anti_debug': True,
                'sha256': 'abc123def456...',
                'detection_reasons': ['High entropy', 'Packed executable', 'Anti-debug techniques']
            }
        ]
    }
    
    generator = ReportGenerator()
    reports = generator.generate_all_reports(test_data)
    
    print("\n[+] Report generation test completed!")
    print(f"[+] Generated {len(reports)} report(s)")
