from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class URLAnalyzeRequest(BaseModel):
    url: str = Field(..., max_length=2048, description="The URL to analyze")

class NormalizedURL(BaseModel):
    original_url: str
    normalized_url: str
    normalization_changes: List[str]

class Classification(BaseModel):
    label: str
    severity: str
    risk_score: int
    confidence: float

class EvidenceItem(BaseModel):
    id: str
    category: str
    severity: str
    title: str
    description: str
    evidence: Dict[str, Any]

class URLFeatures(BaseModel):
    scheme: str
    hostname: str
    registrable_domain: str
    subdomain_count: int
    is_ip_address: bool
    has_punycode: bool
    url_length: int
    # Many more can be dynamically added to dict representation

class ModelScores(BaseModel):
    lexical_probability: float
    structural_probability: float

class RiskAssessment(BaseModel):
    score: int
    severity: str
    confidence: float

class EngineMetadata(BaseModel):
    name: str = "CyberGuard URL Detection Engine"
    version: str = "1.0.0"

class URLAnalyzeResponse(BaseModel):
    success: bool
    input: NormalizedURL
    classification: Classification
    summary: str
    findings: List[EvidenceItem]
    features: Dict[str, Any]
    model: ModelScores
    risk: RiskAssessment
    recommended_actions: List[str]
    engine: EngineMetadata
