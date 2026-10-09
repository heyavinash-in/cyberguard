# Account Takeover Implementation Plan

## Current Architecture Discovered
- **Backend**: FastAPI app in `backend/app` with endpoints for URL (`/api/predict`), Message (`/api/analyze/message`), and Image (`/api/v1/media/image/analyze`). It uses scikit-learn for ML models (`backend/app/ml/`).
- **Frontend**: Next.js app in `src` using Tailwind, Lucide icons, and a dark/glassmorphism UI theme. The sidebar defines navigation. There's an existing `src/lib/behaviour-analyzer` and `impersonation-analyzer` from previous work, but we will create a completely new and unified end-to-end flow for Account Takeover that strictly adheres to the requested architecture.
- **Risk Calculation**: Exists in separate engines per domain. We'll build `account_risk_engine.py` mirroring the deterministic rule + ML probability + Evidence Fusion architecture.

## Files to Create

### Documentation
- `docs/account-takeover-api.md`
- `docs/account-takeover-architecture.md`
- `docs/account-takeover-implementation.md`
- `docs/account-takeover-final-report.md`

### Backend
- `backend/app/schemas/account.py` (Pydantic requests/responses)
- `backend/app/services/account_baseline_service.py` (Manages synthetic user baselines)
- `backend/app/services/account_feature_extractor.py` (Converts raw telemetry vs baseline into binary/numerical features)
- `backend/app/services/account_rule_engine.py` (Generates deterministic findings based on features)
- `backend/app/ml/train_account_anomaly_model.py` (Script to train the IsolationForest model)
- `backend/app/ml/account_anomaly_engine.py` (Runs the IsolationForest inference)
- `backend/app/services/account_evidence_fusion.py` (or `account_risk_engine.py` - Fuses rules + ML into 0-100 risk score and findings)
- `backend/app/services/account_response_engine.py` (Generates response recommendations based on severity)
- `backend/app/routers/account.py` (FastAPI router for the endpoints, imported into `main.py`)

### Frontend
- `src/app/account-security/page.tsx` (Main UI matching CyberGuard themes)
- `src/lib/account-security-api.ts` (Strongly typed API client)
- Update `src/components/layout/sidebar.tsx` to link to `/account-security`.

### Testing
- `evaluate_account_takeover.py` (Validation script running test cases end-to-end)

## Files to Modify
- `backend/app/main.py`: Add `include_router` for the new account router.
- `src/components/layout/sidebar.tsx`: Add the new page to navigation.

## API Contract
POST `/api/v1/account/analyze`
**Request**: `AccountActivityRequest` containing telemetry (user_id, ip, country, device, login result, mfa usage, etc.). No passwords.
**Response**: `AccountActivityResponse` containing risk_score (0-100), severity, findings/evidence, timeline, recommendations.

## Data Flow
Frontend Form -> `AccountActivityRequest` -> FastAPI -> `account_baseline_service` -> `account_feature_extractor` -> (`account_rule_engine` + `account_anomaly_engine`) -> `account_evidence_fusion` -> `account_response_engine` -> `AccountActivityResponse` -> Frontend Dashboard.

## Model Choice
- **IsolationForest** from scikit-learn. It is lightweight, CPU-friendly, handles multivariate anomaly detection well, and will be combined with deterministic rules.

## Risk Calculation Design
1. Base score derived from isolated features.
2. Rule engine calculates contribution points for specific signals (e.g., NEW_DEVICE).
3. Cross-signal correlation (e.g., NEW_DEVICE + UNUSUAL_TIME + BURST).
4. Evidence Fusion clamps risk score. Maximum points capped to avoid overlapping penalties. Ranges: SAFE (0-24), LOW (25-49), MEDIUM (50-74), HIGH (75-89), CRITICAL (90-100).

## Test Strategy
- Unit tests run via `evaluate_account_takeover.py` against the running server. Tests cover SAFE, Single Anomaly, Multi-Anomaly, Takeover, MFA-only, VPN-only.

## Frontend Flow
- A new form takes telemetry input, with "Simulate Normal" and "Simulate Attack" buttons that automatically fill valid telemetry and submit to the real backend API. The result displays a 0-100 risk HUD, anomaly evidence breakdown, and chronological timeline.
