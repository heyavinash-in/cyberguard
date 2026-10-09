from typing import Dict, Any, List

def evaluate_message_risk(ml_prob: float, features: Dict[str, Any], url_engine_results: List[Dict[str, Any]]) -> dict:
    risk_score = 0
    evidence = []
    
    # 1. Base ML Contribution
    ml_points = int(ml_prob * 45) # Base weight up to 45 points
    
    # Contextual ML Attenuation:
    # If the message mentions security terms but makes NO requests, NO threats, and has NO URLs,
    # it is highly likely to be a benign security notification experiencing dataset bias.
    is_benign_mention = (
        (features.get("has_otp_mention") or features.get("has_credential_mention") or features.get("has_payment_mention") or features.get("has_authority_mention"))
        and not features.get("has_otp_request")
        and not features.get("has_credential_request")
        and not features.get("has_card_request")
        and not features.get("has_payment_request")
        and not features.get("has_urgency")
        and not features.get("has_threat")
        and not features.get("has_url")
        and not features.get("has_authority_claim")
    )
    
    # If it's a completely benign mention, heavily attenuate ML bias
    if is_benign_mention:
        ml_points = int(ml_points * 0.3)
        ml_prob = ml_prob * 0.3 # Adjust for explanation
        
    risk_score += ml_points
    
    if ml_prob > 0.7:
        evidence.append({
            "category": "ML_SIGNAL",
            "severity": "HIGH",
            "message": f"Machine Learning detected strong stylistic or linguistic patterns consistent with phishing/spam.",
            "evidence": {"probability": round(ml_prob, 2)},
            "source": "ml"
        })
        
    se_matches = features.get("se_matches", {})
    
    # Security Advice Negation
    if features.get("has_security_advice"):
        # We don't eliminate risk, but we drop it
        risk_score = int(risk_score * 0.7)
        evidence.append({
            "category": "SECURITY_ADVICE",
            "severity": "SAFE",
            "message": "The message contains protective security advice, reducing likelihood of malicious intent.",
            "evidence": se_matches.get("SECURITY_ADVICE", []),
            "source": "rule"
        })
        
    # 2. Urgency + Threat
    if features.get("has_urgency") or features.get("has_threat"):
        ut_pts = 30 # Base
        if features.get("has_credential_request") or features.get("has_otp_request") or features.get("has_url") or features.get("has_payment_request") or features.get("has_card_request"):
            ut_pts = 50 # Escalates heavily
        
        risk_score += ut_pts
        evidence.append({
            "category": "URGENCY_THREAT",
            "severity": "HIGH" if ut_pts >= 40 else "MEDIUM",
            "message": "The message creates time pressure or threatens negative consequences to force immediate action.",
            "evidence": se_matches.get("URGENCY_PRESSURE", []) + se_matches.get("THREAT_OR_CONSEQUENCE", []),
            "source": "rule"
        })
        
    # 3. Credential & OTP Context
    if features.get("has_credential_request") or features.get("has_otp_request") or features.get("has_card_request"):
        cred_pts = 40 # Reaches MEDIUM immediately
        
        # Action + Impersonation Combinations
        if features.get("has_authority_claim"):
            cred_pts = 75 # STRONG_SECURITY_HARVESTING
        elif features.get("has_urgency") or features.get("has_threat") or features.get("has_url"):
            cred_pts = 75
            
        # Security advice overrides some points if it triggered mistakenly
        if features.get("has_security_advice"):
            cred_pts = int(cred_pts * 0.5)
            
        risk_score += cred_pts
        evidence.append({
            "category": "CREDENTIAL_HARVESTING_REQUEST",
            "severity": "CRITICAL" if cred_pts >= 60 else "HIGH",
            "message": "The message explicitly requests sensitive authentication or card information.",
            "evidence": se_matches.get("CREDENTIAL_REQUEST", []) + se_matches.get("OTP_REQUEST", []) + se_matches.get("CARD_DETAILS_REQUEST", []),
            "source": "rule"
        })
    elif features.get("has_credential_mention") or features.get("has_otp_mention"):
        # Mentions are usually benign security alerts (e.g. "Your OTP is 123")
        cred_pts = 5
        if features.get("has_url"):
            cred_pts = 15
        risk_score += cred_pts
        
        if cred_pts > 5:
            evidence.append({
                "category": "CREDENTIAL_MENTION",
                "severity": "LOW",
                "message": "The message mentions security credentials, which is typical of both alerts and phishing.",
                "evidence": se_matches.get("CREDENTIAL_MENTION", []) + se_matches.get("OTP_MENTION", []),
                "source": "rule"
            })
        
    # 4. Financial Context
    if features.get("has_financial_transfer"):
        trans_pts = 15
        if features.get("has_authority_claim") or features.get("has_threat") or features.get("has_urgency"):
            trans_pts = 65
            
        risk_score += trans_pts
        if trans_pts >= 65:
            evidence.append({
                "category": "FINANCIAL_TRANSFER_MANIPULATION",
                "severity": "CRITICAL" if features.get("has_threat") and features.get("has_authority_claim") else "HIGH",
                "message": "The message attempts to manipulate the user into transferring funds, often under the guise of an investigation or security threat.",
                "evidence": se_matches.get("FINANCIAL_TRANSFER_MANIPULATION", []),
                "source": "rule"
            })
            
    if features.get("has_payment_request") or features.get("has_reward"):
        fin_pts = 35 # Base
        
        if features.get("has_authority_claim"):
            fin_pts = 65 # STRONG_FINANCIAL_MANIPULATION / SCAM
        elif features.get("has_url") or features.get("has_urgency") or features.get("has_threat"):
            fin_pts = 60
            
        risk_score += fin_pts
        evidence.append({
            "category": "FINANCIAL_MANIPULATION",
            "severity": "HIGH" if fin_pts >= 50 else "MEDIUM",
            "message": "The message uses financial incentives, prizes, or payment demands as a lure.",
            "evidence": se_matches.get("FINANCIAL_REQUEST", []) + se_matches.get("REWARD_LURE", []),
            "source": "rule"
        })
    elif features.get("has_payment_mention"):
        fin_pts = 5
        risk_score += fin_pts
        
    # 5. Authority Impersonation
    # 5. Authority Impersonation
    if features.get("has_authority_claim"):
        auth_pts = 20 # Level 1
        cat_label = "IDENTITY_IMPERSONATION_CLAIM"
        sev_label = "MEDIUM"
        
        has_req = features.get("has_credential_request") or features.get("has_payment_request") or features.get("has_otp_request") or features.get("has_card_request")
        has_ut = features.get("has_urgency") or features.get("has_threat")
        
        if has_req and has_ut: # Level 4
            auth_pts = 60
            cat_label = "IDENTITY_IMPERSONATION"
            sev_label = "CRITICAL"
        elif has_req: # Level 3
            auth_pts = 45
            cat_label = "IDENTITY_IMPERSONATION"
            sev_label = "HIGH"
        elif has_ut or features.get("has_url"): # Level 2
            auth_pts = 35
            sev_label = "HIGH"
        
        if features.get("sender_suspicious"):
            auth_pts += 15
            
        risk_score += auth_pts
        evidence.append({
            "category": cat_label,
            "severity": sev_label,
            "message": "The message claims to be from a trusted organization (e.g., support, security team).",
            "evidence": se_matches.get("AUTHORITY_CLAIM", []),
            "source": "rule"
        })
    elif features.get("has_authority_mention"):
        auth_pts = 5
        # If it's just mentioning a brand but also requesting OTP/passwords, it elevates
        if features.get("has_credential_request") or features.get("has_otp_request") or features.get("has_payment_request") or features.get("has_card_request"):
            auth_pts = 20
        risk_score += auth_pts
        if auth_pts > 5:
            evidence.append({
                "category": "AUTHORITY_MENTION",
                "severity": "MEDIUM",
                "message": "The message mentions a well-known brand.",
                "evidence": se_matches.get("AUTHORITY_MENTION", []),
                "source": "rule"
            })

    # 6. Structural Adversarial
    if features.get("has_excessive_spacing") or features.get("has_leet_speak") or features.get("normalization_findings"):
        adv_pts = 20
        risk_score += adv_pts
        evidence.append({
            "category": "EVASION",
            "severity": "MEDIUM",
            "message": "The message uses structural evasion techniques like leetspeak, spacing, or fragmentation.",
            "evidence": features.get("normalization_findings", []),
            "source": "rule"
        })

    # 7. URL Engine Integration (Contextual Fusion)
    url_risk_points = 0
    highest_url_severity = "SAFE"
    
    if url_engine_results:
        max_url_score = max(r["risk_score"] for r in url_engine_results)
        
        # Fusion Mapping
        if max_url_score < 20:
            url_risk_points = 0
        elif max_url_score < 40:
            url_risk_points = 10
        elif max_url_score < 60:
            url_risk_points = 25
        elif max_url_score < 80:
            url_risk_points = 45
        else:
            url_risk_points = 60
            
        # Escalation bonus for dangerous combinations
        if max_url_score >= 60 and (features.get("has_credential_request") or features.get("has_otp_request") or features.get("has_payment_request") or features.get("has_card_request") or features.get("has_threat") or features.get("has_authority_claim")):
            url_risk_points += 15
            
        risk_score += url_risk_points
        
        for r in url_engine_results:
            if r["risk_score"] == max_url_score:
                highest_url_severity = r["severity"]
                break
                
        evidence.append({
            "category": "URL_SIGNAL",
            "severity": highest_url_severity,
            "message": "The embedded URL was analyzed by the CyberGuard URL Detection Engine.",
            "evidence": {"max_url_risk": max_url_score, "urls_analyzed": len(url_engine_results)},
            "source": "url_engine"
        })
        
    # Cap at 100
    risk_score = min(risk_score, 100)
    
    # Severity Mapping
    if risk_score < 20:
        severity = "SAFE"
        classification = "BENIGN"
    elif risk_score < 40:
        severity = "LOW"
        classification = "BENIGN" # Low risk means probably benign spam/promo
    elif risk_score < 60:
        severity = "MEDIUM"
        classification = "SUSPICIOUS"
    elif risk_score < 80:
        severity = "HIGH"
        classification = "PHISHING"
    else:
        severity = "CRITICAL"
        classification = "PHISHING"
        
    # Confidence calculation based on evidence volume and agreement
    confidence = 0.5 + (len(evidence) * 0.1)
    if risk_score >= 80 and url_risk_points > 40:
        confidence = min(0.99, confidence + 0.15) # Strong agreement between message rules and URL engine
    elif ml_prob > 0.8 and risk_score >= 60:
        confidence = min(0.95, confidence + 0.1)
    else:
        confidence = min(0.85, confidence)
        
    # Recommendations
    recommendations = []
    if classification == "PHISHING":
        if features.get("has_url"):
            recommendations.append("Do not click any included links.")
        if features.get("has_credential_request") or features.get("has_otp_request") or features.get("has_card_request"):
            recommendations.append("Do not provide passwords, OTPs, or personal information.")
        recommendations.append("Report or block the sender and verify the request directly through the organization's official channels.")
    elif classification == "SUSPICIOUS":
        recommendations.append("Avoid clicking links or sharing personal information.")
        recommendations.append("Verify the sender through an official channel before proceeding.")
    else:
        recommendations.append("No immediate action required.")
        if features.get("has_url"):
            recommendations.append("Continue to exercise standard caution before clicking unfamiliar links.")
            
    return {
        "risk_score": risk_score,
        "severity": severity,
        "classification": classification,
        "confidence": round(confidence, 2),
        "evidence": evidence,
        "recommendations": recommendations
    }
