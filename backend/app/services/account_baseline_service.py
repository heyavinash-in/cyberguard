from typing import Dict, Any

class AccountBaselineService:
    def __init__(self):
        # In-memory mock database of baselines for hackathon prototype
        self._baselines = {
            "user_001": {
                "user_id": "user_001",
                "known_countries": ["India"],
                "known_cities": ["Bhubaneswar"],
                "known_devices": ["device_windows_01", "device_android_01"],
                "known_ips": ["203.0.113.10"],
                "usual_login_hours": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                "average_daily_logins": 4,
                "usual_active_sessions": 1,
                "known_mfa_device": "mfa_device_01"
            }
        }

    def get_baseline(self, user_id: str) -> Dict[str, Any]:
        """Retrieve baseline for a user, or create a blank safe one if none exists."""
        if user_id in self._baselines:
            return self._baselines[user_id]
        return {
            "user_id": user_id,
            "known_countries": [],
            "known_cities": [],
            "known_devices": [],
            "known_ips": [],
            "usual_login_hours": list(range(24)), # Everything is usual for new user to avoid false positives
            "average_daily_logins": 1,
            "usual_active_sessions": 1,
            "known_mfa_device": ""
        }

    def compare_event(self, event: Any) -> Dict[str, str]:
        """Compares current event against the baseline, returning status of each feature."""
        baseline = self.get_baseline(event.user_id)
        
        comparison = {}
        
        if not baseline["known_countries"] or event.country in baseline["known_countries"]:
            comparison["country"] = "KNOWN"
        else:
            comparison["country"] = "NEW"

        if not baseline["known_ips"] or event.ip_address in baseline["known_ips"]:
            comparison["ip"] = "KNOWN"
        else:
            comparison["ip"] = "NEW"

        if not baseline["known_devices"] or event.device_id in baseline["known_devices"]:
            comparison["device"] = "KNOWN"
        else:
            comparison["device"] = "NEW"

        hour = event.timestamp.hour
        if not baseline["usual_login_hours"] or hour in baseline["usual_login_hours"]:
            comparison["login_hour"] = "NORMAL"
        else:
            comparison["login_hour"] = "UNUSUAL"

        return comparison
