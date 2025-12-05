#!/usr/bin/env python3
"""
iOS Network Configuration Validator
Simulates network diagnostics for iOS devices
"""

import json
import random
import socket
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple

class NetworkValidator:
    def __init__(self, device_id: str = None):
        self.device_id = device_id or f"ios-sim-{random.randint(1000, 9999)}"
        self.results = {
            "device_id": self.device_id,
            "timestamp": datetime.now().isoformat(),
            "health_score": 0,
            "issues": [],
            "recommendations": []
        }
    
    def check_wifi_connectivity(self) -> Dict:
        """Simulate Wi-Fi connectivity check"""
        wifi_status = {
            "connected": random.choice([True, True, True, False]),  # 75% success rate
            "signal_strength": random.randint(-80, -30),
            "ssid": "Corporate_WiFi" if random.random() > 0.3 else None,
            "ip_address": f"192.168.1.{random.randint(2, 254)}" if random.random() > 0.2 else None
        }
        
        if not wifi_status["connected"]:
            self.results["issues"].append({
                "category": "Wi-Fi",
                "severity": "high",
                "message": "Device not connected to Wi-Fi",
                "solution": "Connect to corporate Wi-Fi network 'Corp-Employee'"
            })
        elif wifi_status["signal_strength"] < -70:
            self.results["issues"].append({
                "category": "Wi-Fi",
                "severity": "medium",
                "message": f"Weak Wi-Fi signal ({wifi_status['signal_strength']} dBm)",
                "solution": "Move closer to access point or restart Wi-Fi"
            })
        
        return wifi_status
    
    def check_vpn_configuration(self) -> Dict:
        """Validate VPN settings"""
        vpn_configs = [
            {
                "name": "Corporate_VPN",
                "status": random.choice(["connected", "disconnected", "error"]),
                "protocol": "IKEv2",
                "server": "vpn.company.com"
            },
            {
                "name": "Backup_VPN",
                "status": "disabled",
                "protocol": "IPSec",
                "server": "vpn-backup.company.com"
            }
        ]
        
        for vpn in vpn_configs:
            if vpn["status"] == "error":
                self.results["issues"].append({
                    "category": "VPN",
                    "severity": "high",
                    "message": f"VPN {vpn['name']} configuration error",
                    "solution": "Reinstall VPN profile from Company Portal app"
                })
            elif vpn["status"] == "disconnected" and vpn["name"] == "Corporate_VPN":
                self.results["recommendations"].append({
                    "action": "Connect VPN",
                    "priority": "high",
                    "steps": [
                        "Open Settings > VPN",
                        "Toggle Corporate_VPN to ON",
                        "Enter credentials if prompted"
                    ]
                })
        
        return {"vpn_configurations": vpn_configs}
    
    def check_dns_settings(self) -> Dict:
        """Validate DNS configuration"""
        dns_servers = ["8.8.8.8", "8.8.4.4", "10.0.0.1", "10.0.0.2"]
        
        # Simulate DNS resolution test
        test_domains = [
            ("apple.com", True),
            ("company.internal", random.choice([True, False])),
            ("mdm.company.com", random.choice([True, True, False]))  # 66% success
        ]
        
        dns_results = []
        for domain, should_resolve in test_domains:
            if should_resolve:
                dns_results.append({
                    "domain": domain,
                    "status": "resolved",
                    "ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                })
            else:
                dns_results.append({
                    "domain": domain,
                    "status": "failed",
                    "error": "NXDOMAIN"
                })
                if domain == "company.internal":
                    self.results["issues"].append({
                        "category": "DNS",
                        "severity": "high",
                        "message": f"Cannot resolve internal domain: {domain}",
                        "solution": "Update DNS settings to use corporate DNS servers: 10.0.0.1, 10.0.0.2"
                    })
        
        return {
            "dns_servers": dns_servers,
            "resolution_tests": dns_results
        }
    
    def generate_health_report(self) -> Dict:
        """Run all checks and generate comprehensive report"""
        
        print(f"🔍 Starting network diagnostics for device: {self.device_id}")
        
        # Run all checks
        wifi_report = self.check_wifi_connectivity()
        vpn_report = self.check_vpn_configuration()
        dns_report = self.check_dns_settings()
        
        # Calculate health score (0-100)
        issue_count = len(self.results["issues"])
        health_score = max(0, 100 - (issue_count * 20))
        self.results["health_score"] = health_score
        
        # Compile full report
        full_report = {
            **self.results,
            "wifi": wifi_report,
            "vpn": vpn_report,
            "dns": dns_report,
            "summary": {
                "status": "HEALTHY" if health_score >= 80 else "NEEDS_ATTENTION" if health_score >= 50 else "UNHEALTHY",
                "total_checks": 3,
                "passed_checks": 3 - issue_count,
                "failed_checks": issue_count
            }
        }
        
        # Add quick fixes if issues found
        if issue_count > 0:
            full_report["quick_fixes"] = [
                "Restart Wi-Fi: Turn off/on Wi-Fi in Settings",
                "Forget and rejoin corporate network",
                "Restart device if issues persist"
            ]
        
        return full_report
    
    def export_report(self, format: str = "json") -> str:
        """Export report in specified format"""
        report = self.generate_health_report()
        
        if format.lower() == "json":
            return json.dumps(report, indent=2)
        elif format.lower() == "text":
            text_report = f"""
            ════════════════════════════════════════
            iOS NETWORK HEALTH REPORT
            ════════════════════════════════════════
            Device: {report['device_id']}
            Time: {report['timestamp']}
            Health Score: {report['health_score']}/100
            Status: {report['summary']['status']}
            
            ──────────────────────────────────────
            ISSUES FOUND ({len(report['issues'])}):
            ──────────────────────────────────────"""
            
            for i, issue in enumerate(report['issues'], 1):
                text_report += f"\n{i}. [{issue['category']}] {issue['message']}"
                text_report += f"\n   💡 Solution: {issue['solution']}\n"
            
            if report.get('recommendations'):
                text_report += "\n──────────────────────────────────────"
                text_report += "\nRECOMMENDED ACTIONS:"
                text_report += "\n──────────────────────────────────────"
                for rec in report['recommendations']:
                    text_report += f"\n• {rec['action']} ({rec['priority'].upper()} priority)"
            
            return text_report
        else:
            raise ValueError(f"Unsupported format: {format}")

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="iOS Network Configuration Validator")
    parser.add_argument("--device", help="Device identifier")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    parser.add_argument("--export", help="Export to file")
    
    args = parser.parse_args()
    
    validator = NetworkValidator(args.device)
    report = validator.export_report(args.format)
    
    if args.export:
        with open(args.export, 'w') as f:
            f.write(report)
        print(f"Report exported to {args.export}")
    else:
        print(report)

if __name__ == "__main__":
    main()
