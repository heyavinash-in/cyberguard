from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AccountActivityRequest(BaseModel):
    user_id: str
    timestamp: datetime
    ip_address: str
    country: str
    city: Optional[str] = None
    device_id: str
    device_type: str
    login_success: bool
    failed_login_count: int = Field(ge=0)
    mfa_used: bool
    mfa_configuration_changed: bool
    session_id: str
    active_session_count: int = Field(ge=0)
    vpn_detected: bool
    event_description: Optional[str] = None

class Finding(BaseModel):
    finding_id: str
    category: str
    severity: str
    title: str
    explanation: str
    evidence: str
    contribution: int

class TimelineEvent(BaseModel):
    timestamp: datetime
    event: str
    description: str

class AccountActivityResponse(BaseModel):
    request_id: str
    user_id: str
    risk_score: int
    risk_level: str
    classification: str
    confidence: float
    explanation: str
    baseline_comparison: Dict[str, str]
    findings: List[Finding]
    correlations: List[Dict[str, Any]]
    timeline: List[TimelineEvent]
    recommended_actions: List[str]
    model_info: Dict[str, str]
    processing: Dict[str, int]
