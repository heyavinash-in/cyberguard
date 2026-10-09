from typing import Dict, Any, List

class AccountRuleEngine:
    def evaluate(self, features: Dict[str, Any], event: Any) -> List[Dict[str, Any]]:
        findings = []

        if features["new_device"]:
            findings.append({
                "finding_id": "NEW_DEVICE",
                "category": "IDENTITY",
                "severity": "LOW",
                "title": "Unrecognized Device",
                "explanation": f"The device '{event.device_id}' is not in the user's established baseline.",
                "evidence": event.device_id,
                "contribution": 10
            })

        if features["new_ip"]:
            findings.append({
                "finding_id": "NEW_IP",
                "category": "NETWORK",
                "severity": "LOW",
                "title": "Unrecognized IP Address",
                "explanation": f"The IP address '{event.ip_address}' is not in the user's established baseline.",
                "evidence": event.ip_address,
                "contribution": 10
            })

        if features["new_country"]:
            findings.append({
                "finding_id": "NEW_COUNTRY",
                "category": "GEOLOCATION",
                "severity": "MEDIUM",
                "title": "Unusual Geolocation",
                "explanation": f"Login attempt from a new country '{event.country}'.",
                "evidence": event.country,
                "contribution": 20
            })

        if features["unusual_login_hour"]:
            findings.append({
                "finding_id": "UNUSUAL_LOGIN_TIME",
                "category": "BEHAVIOR",
                "severity": "LOW",
                "title": "Unusual Login Time",
                "explanation": f"The login time ({event.timestamp.hour}:00) deviates from historical patterns.",
                "evidence": str(event.timestamp),
                "contribution": 5
            })

        if features["high_failed_login_count"]:
            findings.append({
                "finding_id": "FAILED_LOGIN_BURST",
                "category": "AUTHENTICATION",
                "severity": "HIGH",
                "title": "Authentication Brute Force Indicator",
                "explanation": f"{features['failed_login_count']} failed login attempts detected.",
                "evidence": f"{features['failed_login_count']} failures",
                "contribution": 30
            })

        if features["mfa_configuration_changed"]:
            findings.append({
                "finding_id": "MFA_CONFIGURATION_CHANGE",
                "category": "SECURITY_CONTROL",
                "severity": "HIGH",
                "title": "MFA Configuration Modified",
                "explanation": "Multi-factor authentication settings were modified during this session.",
                "evidence": "MFA Change Detected",
                "contribution": 35
            })

        if features["multiple_active_sessions"]:
            findings.append({
                "finding_id": "MULTIPLE_ACTIVE_SESSIONS",
                "category": "BEHAVIOR",
                "severity": "LOW",
                "title": "Concurrent Sessions",
                "explanation": "User has multiple active sessions across devices.",
                "evidence": f"{event.active_session_count} sessions",
                "contribution": 5
            })

        if features["impossible_travel"]:
            findings.append({
                "finding_id": "IMPOSSIBLE_TRAVEL",
                "category": "GEOLOCATION",
                "severity": "HIGH",
                "title": "Impossible Geographic Transition",
                "explanation": "The distance between the previous and current location is physically implausible given the elapsed time.",
                "evidence": f"New country {event.country} without VPN",
                "contribution": 30
            })

        if features["vpn_detected"]:
            findings.append({
                "finding_id": "VPN_DETECTED",
                "category": "NETWORK",
                "severity": "LOW",
                "title": "Anonymizing Proxy/VPN",
                "explanation": "The IP address is associated with a commercial VPN or proxy.",
                "evidence": event.ip_address,
                "contribution": 0 # VPN alone doesn't add direct malicious risk, just context
            })

        return findings
