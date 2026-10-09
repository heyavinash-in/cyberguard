from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class EvidenceDetail(BaseModel):
    type: str
    strength: str = "NONE"
    severity: str
    description: str
    source: str = "model"

class ModelInfo(BaseModel):
    name: str
    version: str
    inference_ms: int

class ForensicsData(BaseModel):
    frequency: Dict[str, Any] = {}
    compression: Dict[str, Any] = {}
    noise: Dict[str, Any] = {}
    texture: Dict[str, Any] = {}
    statistics: Dict[str, Any] = {}

class ImageAnalysisResponse(BaseModel):
    success: bool
    media_type: str = "image"
    classification: str
    ai_probability: float
    real_probability: float
    confidence: float
    risk_score: int
    severity: str
    evidence: List[EvidenceDetail]
    metadata: Dict[str, Any]
    forensics: ForensicsData
    regions: List[Any] = []
    model: ModelInfo
    recommendations: List[str]
