import time
import uuid
from fastapi import APIRouter, HTTPException
from ..schemas.account import AccountActivityRequest, AccountActivityResponse, TimelineEvent
from ..services.account_baseline_service import AccountBaselineService
from ..services.account_feature_extractor import AccountFeatureExtractor
from ..services.account_rule_engine import AccountRuleEngine
from ..ml.account_anomaly_engine import AccountAnomalyEngine
from ..services.account_risk_engine import AccountRiskEngine
from ..services.account_response_engine import AccountResponseEngine
from ..services.event_store import EventStore

router = APIRouter(prefix="/api/v1/account", tags=["account"])

# Instantiation
baseline_service = AccountBaselineService()
feature_extractor = AccountFeatureExtractor()
rule_engine = AccountRuleEngine()
anomaly_engine = AccountAnomalyEngine()
risk_engine = AccountRiskEngine()
response_engine = AccountResponseEngine()
event_store = EventStore()

@router.post("/analyze", response_model=AccountActivityResponse)
async def analyze_account_activity(request: AccountActivityRequest):
    start_time = time.time()
    
    try:
        # 1. Baseline Comparison
        comparison = baseline_service.compare_event(request)
        
        # 2. Feature Extraction
        features = feature_extractor.extract_features(request, comparison)
        
        # 3. Rule Engine (Deterministic evidence generation)
        findings = rule_engine.evaluate(features, request)
        
        # 4. ML Anomaly Detection (IsolationForest)
        ml_score = anomaly_engine.evaluate(features)
        
        # 5. Risk & Correlation Engine
        final_score, risk_level, classification, confidence, correlations, explanation = risk_engine.fuse_evidence(
            findings, ml_score
        )
        
        # 6. Timeline Generation
        timeline = []
        if request.failed_login_count > 0:
            timeline.append(TimelineEvent(
                timestamp=request.timestamp,
                event="Failed Login Attempt(s)",
                description=f"{request.failed_login_count} failed login attempts recorded."
            ))
        if features["new_ip"] or features["new_device"] or features["new_country"]:
            timeline.append(TimelineEvent(
                timestamp=request.timestamp,
                event="New Environment Context",
                description="Session established from unrecognized context (device/IP/location)."
            ))
        if request.mfa_configuration_changed:
            timeline.append(TimelineEvent(
                timestamp=request.timestamp,
                event="MFA Configuration Change",
                description="User modified their Multi-Factor Authentication settings."
            ))
            
        if not timeline:
            timeline.append(TimelineEvent(
                timestamp=request.timestamp,
                event="Login Success",
                description="User logged in successfully without notable events."
            ))
            
        # Ensure timeline is chronologically sorted (though here they all share the request timestamp for simplicity)
        timeline.sort(key=lambda x: x.timestamp)
        
        # 7. Recommended Response
        recommendations = response_engine.get_recommendations(risk_level)
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        response = AccountActivityResponse(
            request_id=str(uuid.uuid4()),
            user_id=request.user_id,
            risk_score=final_score,
            risk_level=risk_level,
            classification=classification,
            confidence=confidence,
            explanation=explanation,
            baseline_comparison=comparison,
            findings=findings,
            correlations=correlations,
            timeline=timeline,
            recommended_actions=recommendations,
            model_info={
                "anomaly_detector": "IsolationForest",
                "model_version": "v1.0",
                "rule_engine_version": "v1.0"
            },
            processing={
                "latency_ms": latency_ms
            }
        )
        
        event_store.record_event({
            "request_id": response.request_id,
            "engine": "account",
            "input_type": "telemetry",
            "classification": classification,
            "risk_score": final_score,
            "risk_level": risk_level,
            "summary": explanation,
            "raw_result": response.model_dump(mode='json')
        })
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An error occurred during account analysis.")
