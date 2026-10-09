from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class MessageAnalyzeRequest(BaseModel):
    message: str
    sender: Optional[str] = None
    subject: Optional[str] = None
    source: Optional[str] = None

class URLEvidence(BaseModel):
    url: str
    risk_score: int
    severity: str

class Finding(BaseModel):
    category: str
    severity: str
    message: str
    evidence: Optional[Any] = None
    source: str

class MLSignal(BaseModel):
    model_version: str
    probability: float

class MessageClassification(BaseModel):
    label: str
    severity: str
    risk_score: int
    confidence: float

class MessageAnalyzeResponse(BaseModel):
    success: bool
    classification: str
    risk_score: int
    severity: str
    confidence: float
    ml: MLSignal
    message_features: Dict[str, Any]
    extracted_urls: List[URLEvidence]
    findings: List[Finding]
    recommended_response: List[str]
    engine_version: str
