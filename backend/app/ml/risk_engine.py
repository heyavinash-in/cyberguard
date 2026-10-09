from typing import Dict, Any, List

def evaluate_risk(ml_lexical_prob: float, ml_structural_prob: float, features: dict) -> dict:
    risk_score = 0
    evidence = []
    
    # 1. Base ML Contribution
    fused_ml_prob = (ml_lexical_prob * 0.6) + (ml_structural_prob * 0.4)
    # Give ML up to 40 points normally. If it's very confident (>0.8), up to 50.
    ml_points = int(fused_ml_prob * 50) 
    
    # If the domain is officially recognized as legitimate, suppress the ML score substantially.
    if features.get("legit_brand"):
        ml_points = int(fused_ml_prob * 10) 
        
    risk_score += ml_points
    
    if fused_ml_prob > 0.6 and not features.get("legit_brand"):
        evidence.append({
            "id": "ML_PHISHING_SIGNAL",
            "category": "ML_SIGNAL",
            "severity": "HIGH",
            "title": "Machine Learning Threat Detection",
            "description": f"The ML model detected patterns consistent with phishing (probability: {fused_ml_prob:.2f}).",
            "evidence": {"lexical_prob": ml_lexical_prob, "structural_prob": ml_structural_prob}
        })
        
    # 2. Identity Impersonation (Grouped to prevent double counting)
    impersonation_points = 0
    imp_reasons = []
    has_impersonation = False
    
    if features.get("brand_in_subdomain"):
        impersonation_points = max(impersonation_points, 25)
        imp_reasons.append(f"Brand name '{features.get('suspected_brand')}' in subdomain")
        has_impersonation = True
        
    if features.get("brand_impersonation"):
        impersonation_points = max(impersonation_points, 35)
        imp_reasons.append(f"Brand name '{features.get('suspected_brand')}' embedded in an unrelated domain")
        has_impersonation = True
        
    if features.get("typosquatting"):
        impersonation_points = max(impersonation_points, 45)
        imp_reasons.append(f"Look-alike domain mimicking '{features.get('suspected_brand')}' (Similarity: {features.get('typo_similarity')})")
        has_impersonation = True
        
    if impersonation_points > 0:
        risk_score += impersonation_points
        evidence.append({
            "id": "TYPOSQUATTING" if features.get("typosquatting") else "BRAND_IMPERSONATION",
            "category": "IDENTITY_IMPERSONATION",
            "severity": "CRITICAL" if impersonation_points >= 40 else "HIGH",
            "title": "Possible look-alike domain" if features.get("typosquatting") else "Possible Brand Impersonation",
            "description": "The registrable domain closely resembles a known brand domain or uses the brand name deceptively, but is not an official domain.",
            "evidence": {
                "candidate_domain": features.get("registrable_domain"),
                "suspected_brand": features.get("suspected_brand"),
                "indicators": imp_reasons,
                "similarity": features.get("typo_similarity") if features.get("typosquatting") else None
            }
        })
        
    # 3. Authentication Lure (Contextual)
    if features.get("kw_auth") or features.get("kw_urgency"):
        # Base auth points are very low (weak evidence)
        auth_pts = 10 
        
        # Contextual escalation
        if has_impersonation:
            auth_pts = 25 # Strong when combined with impersonation
        elif features.get("is_ip_address"):
            auth_pts = 25 # Strong when combined with raw IP
        elif features.get("obfuscation") or features.get("excessive_encoding") or features.get("nested_url"):
            auth_pts = 20
        elif features.get("suspicious_tld"):
            auth_pts = 15
            
        if features.get("legit_brand"):
            auth_pts = 0 # Suppress auth lure penalty on official domains
            
        risk_score += auth_pts
        if auth_pts > 0:
            evidence.append({
                "id": "AUTHENTICATION_LURE",
                "category": "SOCIAL_ENGINEERING",
                "severity": "HIGH" if auth_pts >= 20 else "LOW",
                "title": "Suspicious Authentication Request",
                "description": "The URL contains terminology commonly used to trick users into providing credentials.",
                "evidence": {"auth_keywords": features.get("kw_auth")}
            })
            
    # 4. Domain / Structural Anomaly
    anomaly_pts = 0
    anomalies = []
    
    if features.get("is_ip_address"):
        ip_pts = 15 # Moderate by itself
        if features.get("kw_auth") or features.get("suspicious_file_ext"):
            ip_pts = 35 # High when hosting a login or executable
        anomaly_pts = max(anomaly_pts, ip_pts)
        anomalies.append("Bare IP Address usage")
        
    if features.get("has_punycode"):
        anomaly_pts = max(anomaly_pts, 15)
        anomalies.append("Punycode (Internationalized Domain) usage")
        
    if features.get("suspicious_tld"):
        tld_pts = 5
        if has_impersonation or features.get("kw_auth"):
            tld_pts = 15
        anomaly_pts = max(anomaly_pts, tld_pts)
        anomalies.append("Suspicious Top-Level Domain")
        
    if anomaly_pts > 0:
        risk_score += anomaly_pts
        evidence.append({
            "id": "DOMAIN_ANOMALY",
            "category": "URL_STRUCTURE",
            "severity": "HIGH" if anomaly_pts >= 25 else "MEDIUM",
            "title": "Domain Structure Anomaly",
            "description": "The domain exhibits structural anomalies often associated with disposable or evasive infrastructure.",
            "evidence": {"anomalies": anomalies}
        })
        
    # 5. Obfuscation
    obf_pts = 0
    obf_reasons = []
    if features.get("nested_url"):
        # Contextual: nested URL + impersonation/auth is worse
        obf_pts = max(obf_pts, 25 if (has_impersonation or features.get("kw_auth")) else 15)
        obf_reasons.append("Nested redirect URL")
    if features.get("excessive_encoding"):
        obf_pts = max(obf_pts, 10)
        obf_reasons.append("Excessive URL encoding")
        
    if obf_pts > 0:
        risk_score += obf_pts
        evidence.append({
            "id": "OBFUSCATION",
            "category": "EVASION",
            "severity": "HIGH" if obf_pts >= 20 else "MEDIUM",
            "title": "URL Obfuscation",
            "description": "The URL contains patterns designed to hide the true destination.",
            "evidence": {"techniques": obf_reasons}
        })
        
    # 6. Malicious Payload (Contextual)
    if features.get("suspicious_file_ext"):
        payload_pts = 20 # Moderate by itself
        if has_impersonation or features.get("is_ip_address") or features.get("suspicious_tld"):
            payload_pts = 40 # Extremely dangerous if impersonating
            
        risk_score += payload_pts
        evidence.append({
            "id": "MALICIOUS_PAYLOAD",
            "category": "PAYLOAD",
            "severity": "CRITICAL" if payload_pts >= 30 else "HIGH",
            "title": "Suspicious File Extension",
            "description": "The URL directly references an executable or archive file extension commonly used for malware delivery.",
            "evidence": {}
        })

    # Legitimate Domain Final Dampening
    # If official brand with no sub-impersonations, forcefully cap risk.
    if features.get("legit_brand"):
        risk_score = min(risk_score, 15)

    # Cap at 100
    risk_score = min(risk_score, 100)
    
    # Severity Mapping
    if risk_score < 20:
        severity = "SAFE"
        classification = "LEGITIMATE"
    elif risk_score < 40:
        severity = "LOW"
        classification = "SUSPICIOUS"
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
    if features.get("legit_brand"):
        confidence = 0.99 
    elif risk_score >= 80:
        confidence = min(0.99, confidence + 0.1)
    else:
        confidence = min(0.85, confidence)
        
    return {
        "risk_score": risk_score,
        "severity": severity,
        "classification": classification,
        "confidence": round(confidence, 2),
        "evidence": evidence
    }
