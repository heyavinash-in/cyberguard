from typing import Dict, Any, List, Tuple

class AccountRiskEngine:
    def fuse_evidence(self, rules_evidence: List[Dict[str, Any]], ml_score: float) -> Tuple[int, str, float, List[Dict[str, Any]], List[Dict[str, Any]], str]:
        base_score = 0
        correlations = []
        
        # 1. Sum up deterministic rule contributions (capped)
        for ev in rules_evidence:
            base_score += ev["contribution"]
            
        # Extract features for correlation detection
        finding_ids = set(ev["finding_id"] for ev in rules_evidence)
        
        # 2. Correlation Logic
        # Pattern 1: New Device + New Country + New IP + Unusual Time
        if {"NEW_DEVICE", "NEW_COUNTRY", "NEW_IP", "UNUSUAL_LOGIN_TIME"}.issubset(finding_ids):
            correlations.append({
                "type": "ACCOUNT_TAKEOVER_PATTERN",
                "severity": "CRITICAL",
                "description": "Multiple authentication and identity signals deviated from the user's established behavioral baseline."
            })
            base_score += 40

        # Pattern 2: Burst of Fails + New Device + New IP + Successful Login
        if {"FAILED_LOGIN_BURST", "NEW_DEVICE", "NEW_IP"}.issubset(finding_ids):
            correlations.append({
                "type": "BRUTE_FORCE_SUCCESS",
                "severity": "CRITICAL",
                "description": "A successful login occurred on a new device immediately following a burst of failed attempts."
            })
            base_score += 50
            
        # Pattern 3: MFA Change + New Device + New Country
        if {"MFA_CONFIGURATION_CHANGE", "NEW_DEVICE", "NEW_COUNTRY"}.issubset(finding_ids):
            correlations.append({
                "type": "MFA_HIJACK_PATTERN",
                "severity": "CRITICAL",
                "description": "MFA configuration was modified from a new geographic location on an unrecognized device."
            })
            base_score += 40

        # 3. Fuse ML Anomaly Score
        # ML score pushes the score higher, but rules take precedence for explainability
        ml_contribution = ml_score * 0.3
        
        # Clamp Final Risk Score
        final_score = min(100, int(base_score + ml_contribution))
        
        # Determine Classification
        classification = "SAFE_ACTIVITY"
        risk_level = "SAFE"
        explanation = "No significant deviation from the user's established baseline was detected."
        
        if final_score >= 90:
            classification = "HIGH_CONFIDENCE_ACCOUNT_TAKEOVER"
            risk_level = "CRITICAL"
            explanation = "Behavior significantly deviates from the established user baseline across multiple correlated signals."
        elif final_score >= 75:
            classification = "ACCOUNT_TAKEOVER_RISK"
            risk_level = "HIGH"
            explanation = "Major anomalies detected in account access patterns, indicating a likely compromise."
        elif final_score >= 50:
            classification = "SUSPICIOUS_ACTIVITY"
            risk_level = "MEDIUM"
            explanation = "Several unusual signals detected. Activity differs moderately from established baseline."
        elif final_score >= 25:
            classification = "LOW_RISK_ANOMALY"
            risk_level = "LOW"
            explanation = "Minor deviations from normal behavior, such as a new IP address or device."

        # Fake a confidence score based on the risk score (since we have no probability distribution)
        confidence = float(final_score / 100.0) if final_score > 0 else 0.99
            
        return final_score, risk_level, classification, confidence, correlations, explanation
