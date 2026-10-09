# Account Takeover Detection Architecture

## Logical Flow

```
NEXT.JS FRONTEND
       ↓
ACCOUNT ACTIVITY FORM
       ↓
POST /api/v1/account/analyze
       ↓
PYDANTIC VALIDATION
       ↓
BASELINE SERVICE (Compares telemetry to user history)
       ↓
FEATURE EXTRACTION (Vectorizes anomalies)
       ↓
┌─────────────────────────────┐
│ Behavioral Rule Engine      │
│ Isolation Forest (ML)       │
│ Correlation Engine          │
└──────────────┬──────────────┘
       ↓
EVIDENCE FUSION (Clamps scores, applies thresholds)
       ↓
RISK ENGINE 0–100
       ↓
CLASSIFICATION ENGINE
       ↓
EXPLANATION ENGINE
       ↓
RESPONSE ENGINE
       ↓
JSON RESPONSE
       ↓
NEXT.JS DASHBOARD
```
