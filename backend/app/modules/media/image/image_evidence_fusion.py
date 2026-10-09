from typing import Dict, Any, Tuple, List
from .schemas import EvidenceDetail

def fuse_evidence(model_classification: str, 
                  model_ai_prob: float, 
                  model_real_prob: float,
                  forensics: Dict[str, Any],
                  metadata: Dict[str, Any]) -> Tuple[str, float, float, float, List[EvidenceDetail]]:
    """
    Fuses the pre-trained model probability with lightweight forensic signals and provenance.
    Outputs the final Authenticity Assessment.
    """
    evidence = []
    
    # Base probabilities from model
    fused_ai_prob = model_ai_prob
    fused_real_prob = model_real_prob
    
    # Gather anomalies
    freq_anomaly = forensics.get("frequency", {}).get("frequency_anomaly", "NONE")
    noise_anomaly = forensics.get("noise", {}).get("noise_anomaly", "NONE")
    comp_anomaly = forensics.get("compression", {}).get("compression_anomaly", "NONE")
    
    # Calculate a simple "forensic strength" supporting AI generation
    # We only treat STRONG/MODERATE as actual signal
    forensic_ai_score = 0
    if freq_anomaly == "STRONG": forensic_ai_score += 2
    elif freq_anomaly == "MODERATE": forensic_ai_score += 1
    
    if noise_anomaly == "STRONG": forensic_ai_score += 2
    elif noise_anomaly == "MODERATE": forensic_ai_score += 1
    
    # Metadata/Provenance
    has_exif = metadata.get("has_exif", False)
    
    # FUSION LOGIC
    # 1. Strong model + supporting forensic evidence -> HIGH confidence
    # 2. Strong model + contradictory forensics -> Reduce confidence
    # 3. Weak model + strong forensic evidence -> UNCERTAIN
    
    final_classification = model_classification
    
    if model_classification == "AI_GENERATED":
        if forensic_ai_score >= 2:
            # Strong model + supporting forensics
            # Slightly boost AI prob, keep as AI_GENERATED
            fused_ai_prob = min(0.99, fused_ai_prob + 0.05)
        elif forensic_ai_score == 0 and has_exif:
            # Strong model but perfectly normal forensics + EXIF
            # Lower confidence slightly, might be a false positive (e.g. digital art)
            fused_ai_prob = max(0.51, fused_ai_prob - 0.15)
            if fused_ai_prob < 0.70:
                final_classification = "UNCERTAIN"
    elif model_classification == "REAL":
        if forensic_ai_score >= 3:
            # Model says REAL, but heavy forensics suggest AI/Synthetic
            # Don't override to AI_GENERATED, just flag as UNCERTAIN
            final_classification = "UNCERTAIN"
            fused_ai_prob = 0.50
            fused_real_prob = 0.50
    elif model_classification == "UNCERTAIN":
        if forensic_ai_score >= 3:
            # Push towards AI if forensics are very strong
            fused_ai_prob = min(0.85, fused_ai_prob + 0.15)
            if fused_ai_prob > 0.80:
                final_classification = "AI_GENERATED"
    
    # Normalize probabilities
    total = fused_ai_prob + fused_real_prob
    if total > 0:
        fused_ai_prob /= total
        fused_real_prob /= total
        
    confidence = max(fused_ai_prob, fused_real_prob)
    
    # Build Explainable Evidence List
    
    # Model Signal
    if final_classification == "AI_GENERATED":
        evidence.append(EvidenceDetail(
            type="MODEL_SIGNAL",
            strength="STRONG" if fused_ai_prob > 0.9 else "MODERATE",
            severity="HIGH",
            description="The image classifier found visual characteristics that are more consistent with synthetic imagery than authentic photography.",
            source="detector_pipeline"
        ))
    elif final_classification == "UNCERTAIN":
        evidence.append(EvidenceDetail(
            type="MODEL_SIGNAL",
            strength="WEAK",
            severity="LOW",
            description="The classifier and fusion engine produced an ambiguous result and could not confidently distinguish authentic from synthetic imagery.",
            source="detector_pipeline"
        ))
    else:
        evidence.append(EvidenceDetail(
            type="MODEL_SIGNAL",
            strength="STRONG" if fused_real_prob > 0.9 else "MODERATE",
            severity="SAFE",
            description="The image classifier found characteristics consistent with authentic photography.",
            source="detector_pipeline"
        ))
        
    # Forensic Evidence
    if freq_anomaly in ["MODERATE", "STRONG"]:
        evidence.append(EvidenceDetail(
            type="FREQUENCY_SIGNAL",
            strength=freq_anomaly,
            severity="MEDIUM" if final_classification == "AI_GENERATED" else "LOW",
            description=f"The image shows {freq_anomaly.lower()} frequency-domain anomalies. This signal is supportive rather than conclusive.",
            source="local_forensic_analysis"
        ))
        
    if noise_anomaly in ["MODERATE", "STRONG"]:
        evidence.append(EvidenceDetail(
            type="NOISE_SIGNAL",
            strength=noise_anomaly,
            severity="MEDIUM" if final_classification == "AI_GENERATED" else "LOW",
            description=f"The image shows {noise_anomaly.lower()} noise distribution anomalies, which can occur in synthetic generation or heavy filtering.",
            source="local_forensic_analysis"
        ))
        
    if not has_exif and final_classification == "AI_GENERATED":
        evidence.append(EvidenceDetail(
            type="IMAGE_METADATA",
            strength="WEAK",
            severity="LOW",
            description="EXIF metadata is missing. While common in compressed images, this supports the synthetic classification.",
            source="metadata_extractor"
        ))
        
    return final_classification, fused_ai_prob, fused_real_prob, confidence, evidence
