from typing import Dict, Any

class AccountFeatureExtractor:
    def extract_features(self, event: Any, comparison: Dict[str, str]) -> Dict[str, Any]:
        """Converts raw telemetry and baseline comparison into numerical/boolean features."""
        
        # Impossible travel heuristic simulation (for hackathon demo)
        # Normally this would calculate haversine distance between last known IP geocoding and current.
        # We will flag it if IP is new, country is new, and VPN is false (simple heuristic).
        impossible_travel = False
        if comparison["country"] == "NEW" and not event.vpn_detected:
            # Fake logic for prototype
            impossible_travel = True

        return {
            "new_ip": comparison["ip"] == "NEW",
            "new_country": comparison["country"] == "NEW",
            "new_device": comparison["device"] == "NEW",
            "unusual_login_hour": comparison["login_hour"] == "UNUSUAL",
            "failed_login_count": event.failed_login_count,
            "high_failed_login_count": event.failed_login_count >= 5,
            "mfa_configuration_changed": event.mfa_configuration_changed,
            "vpn_detected": event.vpn_detected,
            "multiple_active_sessions": event.active_session_count > 1,
            "impossible_travel": impossible_travel,
            "login_success": event.login_success
        }
