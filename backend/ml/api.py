import os
import joblib
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from feature_extractor import URLFeatureExtractor

app = FastAPI(title="CyberGuard ML Service")

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'phishing_model.pkl')
SPAM_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'spam_model.pkl')
SPAM_VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'spam_vectorizer.pkl')

model = None
spam_model = None
spam_vectorizer = None
extractor = URLFeatureExtractor()

@app.on_event("startup")
def load_model():
    global model, spam_model, spam_vectorizer
    if os.path.exists(MODEL_PATH):
        print("Loading URL ML model...")
        model = joblib.load(MODEL_PATH)
    else:
        print("Warning: URL Model not found at", MODEL_PATH)
        
    if os.path.exists(SPAM_MODEL_PATH) and os.path.exists(SPAM_VECTORIZER_PATH):
        print("Loading Spam ML model and vectorizer...")
        with open(SPAM_MODEL_PATH, 'rb') as f:
            spam_model = pickle.load(f)
        with open(SPAM_VECTORIZER_PATH, 'rb') as f:
            spam_vectorizer = pickle.load(f)
    else:
        print("Warning: Spam Model or Vectorizer not found.")

class PredictRequest(BaseModel):
    url: str

class RiskFactor(BaseModel):
    type: str
    severity: str
    title: str
    explanation: str

class PredictResponse(BaseModel):
    prediction: str
    risk_score: int
    confidence: float
    findings: list[RiskFactor]
    features: dict

def generate_findings(features: dict) -> list[dict]:
    findings = []
    
    if features.get('is_ip_address') == 1:
        findings.append({
            "type": "IP_ADDRESS_DOMAIN",
            "severity": "HIGH",
            "title": "IP Address Usage",
            "explanation": "URL uses an IP address instead of a standard domain name, a common phishing tactic."
        })
        
    if features.get('subdomain_manipulation') == 1:
        findings.append({
            "type": "SUBDOMAIN_MANIPULATION",
            "severity": "CRITICAL",
            "title": "Subdomain Manipulation",
            "explanation": "The actual destination of the link is hidden. Phishing links often hide the real domain by adding trusted brand names as subdomains (e.g., paypal.com.security-check.in goes to security-check.in, not PayPal)."
        })
        
    if features.get('impersonation') == 1:
        brand = features.get('impersonated_brand', 'a known brand')
        findings.append({
            "type": "BRAND_IMPERSONATION",
            "severity": "CRITICAL",
            "title": "Domain Spelling / Typosquatting",
            "explanation": f"Attackers often use typosquatting, creating URLs that look almost identical to real brands. This link is impersonating {brand}."
        })

    if features.get('has_unusual_tld') == 1:
        tld = features.get('tld', '')
        findings.append({
            "type": "UNUSUAL_TLD",
            "severity": "MEDIUM",
            "title": "Suspicious Top-Level Domain (TLD)",
            "explanation": f"Legitimate companies usually use common TLDs like .com or .org. Phishing links frequently use cheap or unusual TLDs. This link uses '.{tld}'."
        })

    if features.get('is_shortened') == 1:
        findings.append({
            "type": "URL_SHORTENER",
            "severity": "MEDIUM",
            "title": "Shortened URL Detected",
            "explanation": "Services like Bitly or TinyURL hide the final destination. While legitimate businesses use them, malicious actors heavily rely on them to mask dangerous websites."
        })

    if features.get('is_direct_download') == 1:
        ext = features.get('download_ext', '')
        findings.append({
            "type": "DIRECT_DOWNLOAD",
            "severity": "HIGH",
            "title": "Direct Download Trigger",
            "explanation": f"Safe links usually take you to a readable webpage. Clicking this link immediately prompts a download of a .{ext} file, which is highly likely to be malware."
        })

    if features.get('has_suspicious_words') == 1:
        findings.append({
            "type": "SUSPICIOUS_KEYWORD",
            "severity": "MEDIUM",
            "title": "Contextual Security Keywords",
            "explanation": "URL contains keywords designed to create contextual urgency or panic (e.g., login, secure, verify)."
        })
        
    if features.get('num_subdomains', 0) >= 3 and not features.get('subdomain_manipulation'):
        findings.append({
            "type": "EXCESSIVE_SUBDOMAINS",
            "severity": "LOW",
            "title": "Multiple Subdomains",
            "explanation": "URL contains multiple subdomains, which can be used to obfuscate the real domain."
        })

    if features.get('is_https') == 0:
         findings.append({
            "type": "INSECURE_PROTOCOL",
            "severity": "LOW",
            "title": "HTTPS Status",
            "explanation": "Most secure websites use https://. A link using standard, unencrypted http:// is much more likely to be unsafe."
        })
        
    return findings

@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not model:
        raise HTTPException(status_code=503, detail="Model is not loaded.")
        
    try:
        # 1. Extract Features
        features_dict = extractor.extract_features(req.url)
        vector = extractor.extract_vector(req.url)
        
        # 2. Predict
        prob = model.predict_proba([req.url])[0][1] # Probability of class 1 (phishing)
        
        if features_dict.get('is_legit_brand') == 1 and features_dict.get('subdomain_manipulation') == 0:
            prob = 0.0
            
        # 3. Format Output
        prediction = "PHISHING" if prob > 0.5 else "LEGITIMATE"
        risk_score = int(prob * 100)
        
        findings = generate_findings(features_dict)
        
        return PredictResponse(
            prediction=prediction,
            risk_score=risk_score,
            confidence=prob if prob > 0.5 else (1 - prob),
            findings=findings,
            features=features_dict
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PredictMessageRequest(BaseModel):
    content: str

class PredictMessageResponse(BaseModel):
    prediction: str
    risk_score: int
    confidence: float
    findings: list[RiskFactor]

@app.post("/api/predict-message", response_model=PredictMessageResponse)
def predict_message(req: PredictMessageRequest):
    if not spam_model or not spam_vectorizer:
        raise HTTPException(status_code=503, detail="Spam Model is not loaded.")
        
    try:
        # 1. Extract Features
        text = req.content if req.content else ""
        vector = spam_vectorizer.transform([text])
        
        # 2. Predict (SVC doesn't have predict_proba natively by default, so we use decision_function)
        decision = spam_model.decision_function(vector)[0]
        
        # 3. Convert decision to probability-like score (sigmoid)
        import math
        prob = 1.0 / (1.0 + math.exp(-decision))
        
        prediction = "PHISHING" if prob > 0.5 else "LEGITIMATE"
        risk_score = int(prob * 100)
        
        findings = []
        if risk_score > 60:
            findings.append({
                "type": "MALICIOUS_TEXT_PATTERN",
                "severity": "HIGH",
                "title": "Malicious NLP Pattern Detected",
                "explanation": "Machine Learning model detected structural linguistics and vocabulary heavily associated with spam/phishing."
            })
            
        return PredictMessageResponse(
            prediction=prediction,
            risk_score=risk_score,
            confidence=prob if prob > 0.5 else (1 - prob),
            findings=findings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
