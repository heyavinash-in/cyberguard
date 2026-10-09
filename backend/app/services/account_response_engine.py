from typing import List

class AccountResponseEngine:
    def get_recommendations(self, risk_level: str) -> List[str]:
        if risk_level == "CRITICAL":
            return [
                "Revoke active sessions",
                "Require MFA verification",
                "Force password reset",
                "Block suspicious device",
                "Notify security administrator",
                "Review recent account activity"
            ]
        elif risk_level == "HIGH":
            return [
                "Require MFA verification",
                "Review recent sessions",
                "Notify administrator"
            ]
        elif risk_level == "MEDIUM":
            return [
                "Request additional verification",
                "Monitor active sessions"
            ]
        else:
            return [
                "Continue monitoring"
            ]
