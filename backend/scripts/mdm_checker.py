#!/usr/bin/env python3
"""
MDM & Profile Compliance Checker
Validates iOS device management profiles and security compliance
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List

class MDMComplianceChecker:
    def __init__(self, device_id: str = None):
        self.device_id = device_id or f"ios-mdm-{random.randint(1000, 9999)}"
        self.compliance_rules = self._load_compliance_rules()
        
    def _load_compliance_rules(self) -> Dict:
        """Load corporate compliance rules"""
        return {
            "required_profiles": [
                "Corporate_MDM",
                "VPN_Configuration",
                "Wi-Fi_Certificate",
                "Email_Profile"
            ],
            "security_requirements": {
                "passcode_required": True,
                "min_passcode_length": 6,
                "auto_lock_minutes": 5,
                "encryption_enabled": True,
                "jailbreak_detection": True
            },
            "app_requirements": [
                "Company_Portal",
                "Authenticator",
                "Secure_Mail",
                "VPN_Client"
            ]
        }
    
    def simulate_device_profiles(self) -> Dict:
        """Generate simulated device profile status"""
        base_profiles = [
            {
                "name": "Corporate_MDM",
                "installed": random.choice([True, True, False]),  # 66% installed
                "expiry": (datetime.now() + timedelta(days=random.randint(-10, 90))).isoformat(),
                "organization": "IT Department",
                "identifier": "com.company.mdm.profile"
            },
            {
                "name": "VPN_Configuration",
                "installed": random.choice([True, False]),
                "expiry": (datetime.now() + timedelta(days=random.randint(30, 365))).isoformat(),
                "organization": "Network Team",
                "identifier": "com.company.vpn.profile"
            },
            {
                "name": "Email_Profile",
                "installed": True,
                "expiry": (datetime.now() + timedelta(days=random.randint(60, 365))).isoformat(),
                "organization": "Exchange Team",
                "identifier": "com.company.email.profile"
            }
        ]
        
        # Random additional profiles
        additional_profiles = [
            {
                "name": "Wi-Fi_Certificate",
                "installed": random.choice([True, False]),
                "expiry": (datetime.now() + timedelta(days=random.randint(-5, 180))).isoformat(),
                "organization": "Security Team",
                "identifier": "com.company.wifi.cert"
            },
            {
                "name": "Security_Policy",
                "installed": random.choice([True, True, True, False]),  # 75% installed
                "expiry": (datetime.now() + timedelta(days=random.randint(100, 365))).isoformat(),
                "organization": "Compliance Office",
                "identifier": "com.company.security.policy"
            }
        ]
        
        return base_profiles + additional_profiles
    
    def check_security_compliance(self) -> Dict:
        """Check device security settings"""
        security_status = {
            "passcode": {
                "enabled": random.choice([True, True, True, False]),  # 75% enabled
                "length": random.randint(4, 8),
                "complexity": random.choice(["none", "numeric", "alphanumeric"])
            },
            "auto_lock": {
                "enabled": True,
                "minutes": random.choice([1, 2, 5, 10, 30])
            },
            "encryption": {
                "data_protection": random.choice([True, True, False]),  # 66% enabled
                "filevault": True  # iOS always enabled
            },
            "device": {
                "jailbroken": random.choice([False, False, False, True]),  # 25% chance
                "os_version": f"iOS {random.choice(['16.7', '17.2', '17.3', '17.4'])}",
                "model": random.choice(["iPhone 14 Pro", "iPhone 15", "iPhone 13", "iPad Pro"])
            }
        }
        
        return security_status
    
    def check_app_compliance(self) -> List[Dict]:
        """Check required corporate apps"""
        corporate_apps = [
            {"name": "Company_Portal", "installed": random.choice([True, False]), "version": "4.8.1"},
            {"name": "Authenticator", "installed": random.choice([True, True, False]), "version": "6.7.2"},
            {"name": "Secure_Mail", "installed": random.choice([True, False]), "version": "5.3.0"},
            {"name": "VPN_Client", "installed": random.choice([True, True, True, False]), "version": "3.2.1"},
            {"name": "Teams", "installed": True, "version": "5.9.1"},
            {"name": "OneDrive", "installed": True, "version": "14.8.1"}
        ]
        
        return corporate_apps
    
    def run_compliance_check(self) -> Dict:
        """Run full compliance check"""
        print(f"📱 Running MDM compliance check for: {self.device_id}")
        
        profiles = self.simulate_device_profiles()
        security = self.check_security_compliance()
        apps = self.check_app_compliance()
        
        # Analyze compliance
        compliance_issues = []
        recommendations = []
        
        # Check required profiles
        required_profiles = self.compliance_rules["required_profiles"]
        installed_profiles = [p["name"] for p in profiles if p["installed"]]
        
        for required in required_profiles:
            if required not in installed_profiles:
                compliance_issues.append({
                    "type": "missing_profile",
                    "profile": required,
                    "severity": "high",
                    "action": f"Install {required} profile from Company Portal"
                })
        
        # Check profile expiry
        for profile in profiles:
            if profile["installed"]:
                expiry_date = datetime.fromisoformat(profile["expiry"])
                days_until_expiry = (expiry_date - datetime.now()).days
                if days_until_expiry < 30:
                    compliance_issues.append({
                        "type": "expiring_profile",
                        "profile": profile["name"],
                        "days_remaining": days_until_expiry,
                        "severity": "medium" if days_until_expiry > 7 else "high",
                        "action": f"Renew {profile['name']} profile before expiry"
                    })
        
        # Check security compliance
        if not security["passcode"]["enabled"]:
            compliance_issues.append({
                "type": "security",
                "issue": "Passcode not enabled",
                "severity": "critical",
                "action": "Enable passcode in Settings > Face ID & Passcode"
            })
        
        if security["passcode"]["length"] < 6:
            compliance_issues.append({
                "type": "security",
                "issue": f"Passcode too short ({security['passcode']['length']} characters)",
                "severity": "high",
                "action": "Increase passcode length to at least 6 characters"
            })
        
        if security["device"]["jailbroken"]:
            compliance_issues.append({
                "type": "security",
                "issue": "Device is jailbroken",
                "severity": "critical",
                "action": "Contact IT security immediately. Jailbroken devices cannot access corporate resources."
            })
        
        # Check app compliance
        required_apps = self.compliance_rules["app_requirements"]
        installed_apps = [app["name"] for app in apps if app["installed"]]
        
        for app in required_apps:
            if app not in installed_apps:
                recommendations.append({
                    "type": "app",
                    "app": app,
                    "priority": "medium",
                    "action": f"Install {app} from App Store",
                    "link": "https://apps.company.com/install"
                })
        
        # Calculate compliance score
        total_checks = (
            len(required_profiles) + 
            3 +  # security checks
            len(required_apps)
        )
        failed_checks = len(compliance_issues)
        compliance_score = max(0, 100 - (failed_checks * 100 // total_checks))
        
        report = {
            "device_id": self.device_id,
            "timestamp": datetime.now().isoformat(),
            "compliance_score": compliance_score,
            "status": "COMPLIANT" if compliance_score >= 90 else "NON_COMPLIANT",
            "profiles": profiles,
            "security": security,
            "apps": apps,
            "issues": compliance_issues,
            "recommendations": recommendations,
            "summary": {
                "total_checks": total_checks,
                "passed_checks": total_checks - failed_checks,
                "failed_checks": failed_checks,
                "critical_issues": len([i for i in compliance_issues if i["severity"] == "critical"]),
                "high_priority": len([i for i in compliance_issues if i["severity"] == "high"])
            }
        }
        
        return report
    
    def generate_compliance_certificate(self) -> Dict:
        """Generate a compliance certificate for the device"""
        report = self.run_compliance_check()
        
        certificate = {
            "certificate_id": f"CMP-{random.randint(10000, 99999)}",
            "device_id": report["device_id"],
            "issue_date": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=30)).isoformat(),
            "compliance_status": report["status"],
            "score": report["compliance_score"],
            "issuer": "Corporate IT Compliance Authority",
            "signature": "Verified by Company MDM System",
            "details": {
                "profiles_installed": len([p for p in report["profiles"] if p["installed"]]),
                "security_compliant": report["compliance_score"] >= 80,
                "apps_installed": len([a for a in report["apps"] if a["installed"]])
            }
        }
        
        return certificate

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MDM Compliance Checker")
    parser.add_argument("--device", help="Device identifier")
    parser.add_argument("--certificate", action="store_true", help="Generate compliance certificate")
    parser.add_argument("--export", help="Export to JSON file")
    
    args = parser.parse_args()
    
    checker = MDMComplianceChecker(args.device)
    
    if args.certificate:
        result = checker.generate_compliance_certificate()
    else:
        result = checker.run_compliance_check()
    
    if args.export:
        with open(args.export, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Exported to {args.export}")
    else:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
