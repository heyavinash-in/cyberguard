# CyberGuard URL Detection Engine

## 1. Architecture
The URL detection engine has been refactored into a single coherent, modular, and lightweight pipeline running on FastAPI (`backend/app/main.py`). The frontend (`Next.js`) acts strictly as a display layer and proxy, removing previous conflicting logic.

**Flow:**
`Next.js Proxy` -> `FastAPI /api/predict` -> `Normalizer` -> `StaticFeatureExtractor` -> `ML Models` -> `Risk Engine` -> `JSON Output`

## 2. Data Flow & Feature Extraction
Urls are passed to the `StaticFeatureExtractor`, which breaks them into 30+ numeric features without making any live network requests (SSRF prevention).
Categories include:
- **Lexical/Structural:** Lengths, dot counts, parameter counts.
- **Brand Impersonation:** Typosquatting and subdomain impersonation using `BRAND_CONFIG`.
- **Security:** HTTPS, IP address hostnames, excessive encoding.
- **Social Engineering:** Auth/Financial keywords.

## 3. Dataset Preprocessing & Training
The models are trained using two Hugging Face datasets:
- `alexkstern/phishing_urls`
- `Mitake/PhishingURLsANDBenignURLs`

**Preprocessing:**
- Deduplication by URL.
- 50k stratified sample to balance speed and accuracy.
- 80/20 Train/Test split.

## 4. ML Model Architecture
Instead of a single text model, the engine uses two models to ensure structural features are utilized:
1. **Lexical Model:** `LogisticRegression` on `TfidfVectorizer` (3-5 character n-grams).
2. **Structural Model:** `HistGradientBoostingClassifier` trained directly on the exact numeric output of `StaticFeatureExtractor`.

Both models output calibrated probabilities, which are fused inside the Risk Engine.

## 5. Central Risk Engine
The risk engine (`backend/app/ml/risk_engine.py`) takes the fused ML probability and the deterministic features and groups them to prevent double-counting.
- **Evidence Groups:** `ML_SIGNAL`, `IDENTITY_IMPERSONATION`, `AUTHENTICATION_LURE`, `URL_STRUCTURE`, `EVASION`, `PAYLOAD`.
- **Confidence:** Derived from evidence volume and model agreement.
- **Severity Mapping:** 
  - 0-19: SAFE
  - 20-39: LOW
  - 40-59: MEDIUM
  - 60-79: HIGH
  - 80-100: CRITICAL

## 6. Performance & Testing
- **Inference Latency:** < 50ms per URL.
- **Memory:** CPU-only, models combined are < 5MB RAM.
- **Testing:** Suite runs via `pytest tests/url_engine`.
