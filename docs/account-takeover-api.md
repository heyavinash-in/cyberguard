# Account Takeover API Documentation

## POST /api/v1/account/analyze

Analyzes account activity telemetry against an established behavioral baseline.

### Request Schema (AccountActivityRequest)
```json
{
  "user_id": "user_001",
  "timestamp": "2023-10-24T02:47:00Z",
  "ip_address": "203.0.113.45",
  "country": "Singapore",
  "city": "Singapore",
  "device_id": "device_unknown_99",
  "device_type": "Other",
  "login_success": false,
  "failed_login_count": 7,
  "mfa_used": true,
  "mfa_configuration_changed": true,
  "session_id": "sess_099",
  "active_session_count": 3,
  "vpn_detected": false,
  "event_description": "Multiple failed attempts followed by MFA change"
}
```

### Response Schema (AccountActivityResponse)
```json
{
  "request_id": "req_xyz",
  "user_id": "user_001",
  "risk_score": 91,
  "risk_level": "CRITICAL",
  "classification": "HIGH_CONFIDENCE_ACCOUNT_TAKEOVER",
  "confidence": 0.95,
  "baseline_comparison": {
    "country": "NEW",
    "device": "NEW",
    "ip": "NEW",
    "login_hour": "UNUSUAL"
  },
  "findings": [
    {
      "finding_id": "NEW_DEVICE",
      "category": "IDENTITY",
      "severity": "MEDIUM",
      "title": "Unrecognized Device",
      "explanation": "Device device_unknown_99 is not in the baseline.",
      "evidence": "device_unknown_99",
      "contribution": 15
    }
  ],
  "timeline": [
    {
      "timestamp": "2023-10-24T02:47:00Z",
      "event": "Login Failed",
      "description": "7 failed attempts"
    }
  ],
  "recommended_actions": [
    "Revoke active sessions",
    "Require MFA verification",
    "Force password reset"
  ],
  "model_info": {
    "anomaly_detector": "IsolationForest",
    "model_version": "v1.0",
    "rule_engine_version": "v1.0"
  },
  "processing": {
    "latency_ms": 12
  }
}
```

## Known Limitations
- The system currently uses in-memory synthetic baselines.
- Geolocation distance calculation for impossible travel is simulated using basic heuristic distances between countries/cities unless a mapping database is attached.
