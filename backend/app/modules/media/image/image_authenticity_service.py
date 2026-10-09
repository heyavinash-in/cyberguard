from typing import Dict, Any, Tuple
from PIL import Image

from .image_metadata import extract_image_metadata
from .detector_registry import get_detector
from .schemas import ImageAnalysisResponse, EvidenceDetail, ModelInfo

def map_risk_severity(classification: str, ai_prob: float) -> Tuple[int, str]:
    """
    Map detector classification into CyberGuard risk score & severity.
    """
    if classification == "AI_GENERATED":
        # Base AI generated image is suspicious, but not instantly critical unless context demands it.
        risk = int(60 + (ai_prob * 20)) # 60 - 80 range
        sev = "HIGH" if risk >= 70 else "MEDIUM"
    elif classification == "UNCERTAIN":
        risk = 40
        sev = "LOW"
    else:
        risk = 10
        sev = "SAFE"
        
    return risk, sev



from .image_forensics import run_all_forensics
from .image_evidence_fusion import fuse_evidence

def analyze_image(img: Image.Image, raw_bytes: bytes) -> ImageAnalysisResponse:
    # 1. Metadata
    metadata = extract_image_metadata(img, raw_bytes)
    
    # 2. Forensics
    forensics = run_all_forensics(img, raw_bytes)
    
    # 3. Inference
    detector = get_detector()
    model_classification, model_ai_prob, model_real_prob, model_info_dict = detector.predict(img)
    
    # 4. Evidence Fusion
    classification, ai_prob, real_prob, confidence, evidence = fuse_evidence(
        model_classification, model_ai_prob, model_real_prob, forensics, metadata
    )
    
    # 5. Cyber Risk Fusion
    risk_score, severity = map_risk_severity(classification, ai_prob)
    
    return ImageAnalysisResponse(
        success=True,
        media_type="image",
        classification=classification,
        ai_probability=round(ai_prob, 4),
        real_probability=round(real_prob, 4),
        confidence=round(confidence, 4),
        risk_score=risk_score,
        severity=severity,
        evidence=evidence,
        metadata=metadata,
        forensics=forensics,
        regions=[],
        model=ModelInfo(**model_info_dict),
        recommendations=[]
    )
