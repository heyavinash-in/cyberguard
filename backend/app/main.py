import os
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from .schemas.url import URLAnalyzeRequest, URLAnalyzeResponse
from .services.normalizer import normalize_url
from .services.extractor import StaticFeatureExtractor
from .ml.risk_engine import evaluate_risk
from .routers import account, dashboard, system, cases
import uuid
from .services.event_store import EventStore

app = FastAPI(title="CyberGuard URL Detection Engine", version="1.0.0")

app.include_router(account.router)
app.include_router(dashboard.router)
app.include_router(system.router)
app.include_router(cases.router)

event_store = EventStore()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models')
LEXICAL_MODEL_PATH = os.path.join(MODEL_DIR, 'phishing_lexical_model.pkl')
STRUCTURAL_MODEL_PATH = os.path.join(MODEL_DIR, 'phishing_structural_model.pkl')

lexical_model = None
structural_model = None

@app.on_event("startup")
def load_models():
    global lexical_model, structural_model
    try:
        if os.path.exists(LEXICAL_MODEL_PATH):
            lexical_model = joblib.load(LEXICAL_MODEL_PATH)
        if os.path.exists(STRUCTURAL_MODEL_PATH):
            structural_model = joblib.load(STRUCTURAL_MODEL_PATH)
    except Exception as e:
        print(f"Error loading models: {e}")

extractor = StaticFeatureExtractor()

@app.post("/api/predict", response_model=URLAnalyzeResponse)
async def predict_url(req: URLAnalyzeRequest):
    # 1. Normalize
    norm_result = normalize_url(req.url)
    if "Failed to parse URL" in norm_result.get("normalization_changes", []):
        raise HTTPException(status_code=400, detail="Invalid URL format")
        
    # 2. Extract Features
    features = extractor.extract(norm_result)
    
    # 3. ML Inference
    lexical_prob = 0.0
    structural_prob = 0.0
    
    if lexical_model:
        try:
            lexical_prob = float(lexical_model.predict_proba([norm_result["normalized_url"]])[0][1])
        except Exception:
            pass
            
    if structural_model:
        try:
            # We must map features to the exact numeric array expected by the model
            # For this MVP fallback if structural_model isn't fully trained yet:
            # We'll expect a specific feature ordering.
            feature_keys = [
                "url_length", "hostname_length", "path_length", "num_subdomains", 
                "num_dots", "num_hyphens", "num_special_chars", "is_ip_address",
                "hostname_entropy", "path_entropy"
            ]
            X_struct = np.array([[float(features.get(k, 0)) for k in feature_keys]])
            structural_prob = float(structural_model.predict_proba(X_struct)[0][1])
        except Exception:
            # If structural fails, we just lean on lexical
            pass
            
    # 4. Risk Engine
    risk_assessment = evaluate_risk(lexical_prob, structural_prob, features)
    
    # 5. Recommendations
    recommended_actions = []
    if risk_assessment["severity"] in ["HIGH", "CRITICAL"]:
        recommended_actions.append("Do not enter credentials.")
        recommended_actions.append("Do not provide payment information.")
        recommended_actions.append("Verify the destination through the organization's official website.")
    elif risk_assessment["severity"] == "MEDIUM":
        recommended_actions.append("Proceed with caution.")
        recommended_actions.append("Verify the domain name carefully before submitting any data.")
    else:
        recommended_actions.append("No immediate threats detected.")
        recommended_actions.append("Standard browsing caution is advised.")
        
    summary_text = "This URL shows multiple indicators associated with phishing and impersonation." if risk_assessment["severity"] in ["HIGH", "CRITICAL"] else "The URL appears to be structurally safe."

    response_payload = {
        "success": True,
        "input": norm_result,
        "classification": {
            "label": risk_assessment["classification"],
            "severity": risk_assessment["severity"],
            "risk_score": risk_assessment["risk_score"],
            "confidence": risk_assessment["confidence"]
        },
        "summary": summary_text,
        "findings": risk_assessment["evidence"],
        "features": features,
        "model": {
            "lexical_probability": round(lexical_prob, 4),
            "structural_probability": round(structural_prob, 4)
        },
        "risk": {
            "score": risk_assessment["risk_score"],
            "severity": risk_assessment["severity"],
            "confidence": risk_assessment["confidence"]
        },
        "recommended_actions": recommended_actions,
        "engine": {
            "name": "CyberGuard URL Detection Engine",
            "version": "1.0.0"
        }
    }
    
    event_store.record_event({
        "request_id": str(uuid.uuid4()),
        "engine": "url",
        "input_type": "url",
        "classification": risk_assessment["classification"],
        "risk_score": risk_assessment["risk_score"],
        "risk_level": risk_assessment["severity"],
        "summary": summary_text,
        "raw_result": response_payload
    })

    return response_payload

from .schemas.message import MessageAnalyzeRequest, MessageAnalyzeResponse
from .services.message_extractor import MessageFeatureExtractor
from .ml.message_risk_engine import evaluate_message_risk

# Message Models
MESSAGE_MODEL_PATH = os.path.join(MODEL_DIR, 'message', 'message_ensemble_model.pkl')
message_model = None
msg_extractor = MessageFeatureExtractor()

from .modules.media.image.detector_registry import get_detector

@app.on_event("startup")
def load_msg_models():
    global message_model
    try:
        if os.path.exists(MESSAGE_MODEL_PATH):
            message_model = joblib.load(MESSAGE_MODEL_PATH)
    except Exception as e:
        print(f"Error loading message model: {e}")
        
    print("Pre-loading Media Intelligence AI model...")
    try:
        get_detector().load()
    except Exception as e:
        print(f"Error loading media model: {e}")

# Call the original load_models
load_models()
load_msg_models()

@app.post("/api/analyze/message", response_model=MessageAnalyzeResponse)
async def analyze_message_endpoint(req: MessageAnalyzeRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    # 1. Feature Extraction & SE Rules
    features, extracted_urls = msg_extractor.extract_features(req.message, req.sender, req.subject)
    
    # 2. URL Engine Analysis for extracted URLs
    url_results = []
    for raw_url in extracted_urls:
        try:
            norm_result = normalize_url(raw_url)
            if "Failed to parse URL" not in norm_result.get("normalization_changes", []):
                url_features = extractor.extract(norm_result)
                l_prob = 0.0
                s_prob = 0.0
                if lexical_model:
                    try:
                        l_prob = float(lexical_model.predict_proba([norm_result["normalized_url"]])[0][1])
                    except Exception: pass
                if structural_model:
                    try:
                        f_keys = ["url_length", "hostname_length", "path_length", "num_subdomains", "num_dots", "num_hyphens", "num_special_chars", "is_ip_address", "hostname_entropy", "path_entropy"]
                        x_s = np.array([[float(url_features.get(k, 0)) for k in f_keys]])
                        s_prob = float(structural_model.predict_proba(x_s)[0][1])
                    except Exception: pass
                u_risk = evaluate_risk(l_prob, s_prob, url_features)
                url_results.append({
                    "url": raw_url,
                    "risk_score": u_risk["risk_score"],
                    "severity": u_risk["severity"],
                    "classification": u_risk["classification"]
                })
        except Exception as e:
            print(f"Error processing URL {raw_url}: {e}")
            pass
            
    # 3. ML Inference
    ml_prob = 0.0
    if message_model:
        try:
            from .services.message_extractor import preprocess_text
            clean_msg = preprocess_text(req.message)
            ml_prob = float(message_model.predict_proba([clean_msg])[0][1])
        except Exception as e:
            print(f"ML Error: {e}")
            
    # 4. Message Risk Engine
    risk_assessment = evaluate_message_risk(ml_prob, features, url_results)
    
    response_payload = {
        "success": True,
        "classification": risk_assessment["classification"],
        "risk_score": risk_assessment["risk_score"],
        "severity": risk_assessment["severity"],
        "confidence": risk_assessment["confidence"],
        "ml": {
            "model_version": "message-v1",
            "probability": round(ml_prob, 4)
        },
        "message_features": features,
        "extracted_urls": url_results,
        "findings": risk_assessment["evidence"],
        "recommended_response": risk_assessment["recommendations"],
        "engine_version": "message-v1"
    }

    event_store.record_event({
        "request_id": str(uuid.uuid4()),
        "engine": "message",
        "input_type": "text",
        "classification": risk_assessment["classification"],
        "risk_score": risk_assessment["risk_score"],
        "risk_level": risk_assessment["severity"],
        "summary": "Message flagged for social engineering." if risk_assessment["severity"] in ["HIGH", "CRITICAL"] else "Message appears safe.",
        "raw_result": response_payload
    })

    return response_payload

from fastapi import File, UploadFile
from .modules.media.image import validate_image, analyze_image, ImageAnalysisResponse

@app.post("/api/v1/media/image/analyze", response_model=ImageAnalysisResponse)
async def analyze_image_endpoint(image: UploadFile = File(...)):
    img, raw_bytes = await validate_image(image)
    result = analyze_image(img, raw_bytes)
    
    event_store.record_event({
        "request_id": str(uuid.uuid4()),
        "engine": "media",
        "input_type": "image",
        "classification": result.classification,
        "risk_score": result.risk_score,
        "risk_level": result.severity,
        "summary": "Forensics detected AI anomalies" if result.classification == "AI_GENERATED" else "Image appears to be authentic",
        "raw_result": result.model_dump(mode='json')
    })
    
    return result

