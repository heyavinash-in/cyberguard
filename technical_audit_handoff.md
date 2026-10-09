==================================================
# 1. PROJECT OVERVIEW
==================================================
*   **Project Name**: CyberGuard
*   **Current Project Purpose**: An AI-powered phishing URL and email spam detection engine leveraging machine learning (TF-IDF + Scikit-Learn) and deterministic URL feature extraction.
*   **Current Implementation Status**: The project has been reverted to a baseline ML model architecture. The previously planned complex phased architecture (DNS, external reputation APIs, heuristic rules engine) has been stripped out.
*   **What the application can actually do RIGHT NOW**: 
    *   Accepts a URL string via a Next.js web interface.
    *   Passes it to a FastAPI backend to extract structural features (e.g., entropy, typosquatting, subdomains).
    *   Scores the URL using a serialized Logistic Regression model.
    *   Returns a risk score (0-100), prediction (PHISHING/LEGITIMATE), and hardcoded rule-based findings back to the frontend to display.
*   **Original intended functionality**: Full threat-intelligence fusion layer (Phase 1-8) combining ML, heuristic rules, DNS/PTR lookups, and Reputation providers.
*   **Implemented vs Planned vs Missing**: 
    *   *Implemented*: Next.js UI, FastAPI REST endpoints, URL feature extraction, Scikit-Learn training scripts, URL ML inference.
    *   *Planned/Dead Code*: Gemini API integrations are present in the frontend source but bypassed. 
    *   *Missing*: Databases, external threat feeds, DNS lookups, authentication.
*   **Current major limitations**: Completely stateless (no database). No external network intelligence. Blocks synchronous execution during inference. Model performance relies purely on string parsing.
*   **Current entry points for running the application**:
    *   Frontend: `npm run dev` (starts on port 3000)
    *   Backend: `cd backend/ml && python -m uvicorn api:app --host 127.0.0.1 --port 8000`
*   **Frontend/Backend relationship**: Next.js frontend acts as a proxy/client. The `src/lib/url-analyzer/pipeline.ts` explicitly fetches `http://127.0.0.1:8000/api/predict` via POST.

==================================================
# 2. COMPLETE DIRECTORY TREE
==================================================
*   `/src/app/api/analyze-url/route.ts` - **Purpose**: Next.js API route proxying requests from the browser to the backend. **Used**: Yes.
*   `/src/lib/url-analyzer/pipeline.ts` - **Purpose**: Frontend orchestration logic. Merges client-side rules with the backend ML response. **Used**: Yes. **Dependencies**: `ai-provider.ts` (imported but unused), `parser.ts`, `rule-engine.ts`.
*   `/src/lib/url-analyzer/ai-provider.ts` - **Purpose**: Gemini AI interaction. **Used**: No (Dead code).
*   `/backend/ml/api.py` - **Purpose**: Main FastAPI application serving the ML models. **Used**: Yes. **Dependencies**: `joblib`, `pickle`, `feature_extractor.py`.
*   `/backend/ml/feature_extractor.py` - **Purpose**: `URLFeatureExtractor` class that extracts structural and lexical features from URLs using Regex and parsing. **Used**: Yes.
*   `/backend/ml/train.py` - **Purpose**: Script to download HuggingFace datasets, train a Logistic Regression model on URLs, and save `phishing_model.pkl`. **Used**: Yes (Offline).
*   `/backend/ml/train_message.py` - **Purpose**: Script to train a LinearSVC on the Kaggle SMS Spam dataset. **Used**: Yes (Offline).
*   `/backend/ml/models/` - **Purpose**: Storage for serialized `.pkl` models and `.json` metadata. **Used**: Yes.
*   `/data/` - **Purpose**: Storage for raw `.csv` datasets (if downloaded locally). **Used**: Yes.

==================================================
# 3. COMPLETE TECH STACK
==================================================
### Frontend
*   **Framework**: Next.js (App Router)
*   **React version**: 19.2.8
*   **Next.js version**: 16.3.4
*   **Styling**: TailwindCSS v4, `clsx`, `tailwind-merge`
*   **UI libraries**: Radix UI (`@radix-ui/react-slot`)
*   **Animation libraries**: Framer Motion
*   **Icons**: Lucide React
*   **Charts**: MISSING
*   **HTTP/API clients**: Native `fetch` API

### Backend
*   **Framework**: FastAPI
*   **Python version**: Generic Python 3.x (Detected via standard library usage)
*   **Server**: Uvicorn
*   **API architecture**: RESTful POST endpoints
*   **Authentication**: MISSING
*   **Database**: MISSING
*   **Cache**: MISSING
*   **Background jobs**: MISSING

### Machine Learning
*   **Frameworks**: Scikit-Learn
*   **Algorithms**: Logistic Regression (URL), LinearSVC (Spam/Message)
*   **Libraries**: Pandas, Joblib, Pickle, HuggingFace `datasets`
*   **Feature extraction**: `TfidfVectorizer` (character n-grams 3-5), Custom Python string parsing
*   **Model serialization**: Joblib (`.pkl`), Pickle (`.pkl`)

### Security analysis
*   **URL parsing libraries**: `urllib.parse`, `tldextract`
*   **Domain analysis**: Basic regex/string matching
*   **DNS/TLS analysis**: MISSING
*   **Reputation APIs**: MISSING
*   **Header analysis**: MISSING

### DevOps / Deployment
*   **Docker**: MISSING
*   **Environment variables**: `.env.example`, `.env.local`
*   **CI/CD**: MISSING

==================================================
# 4. SYSTEM ARCHITECTURE
==================================================
USER
↓ (Submits URL via UI)
FRONTEND (`src/app/analyze/page.tsx` or similar component)
↓ (POST JSON)
FRONTEND PROXY (`src/app/api/analyze-url/route.ts`)
↓ (Synchronous `fetch`)
FRONTEND PIPELINE (`src/lib/url-analyzer/pipeline.ts`)
↓ (HTTP POST)
BACKEND API (`backend/ml/api.py` - `predict()`)
↓ (Function call)
FEATURE EXTRACTOR (`backend/ml/feature_extractor.py`)
↓ (Transforms string to dict)
ML MODEL (`model.predict_proba()` via Scikit-Learn)
↓ (Probability float)
RESPONSE FORMATTER (`api.py: generate_findings()`)
↓ (JSON Response)
FRONTEND PIPELINE (`pipeline.ts` merging ML score with UI whitelist)
↓ (JSON)
DASHBOARD

**Architecture Facts:**
*   Model inference is purely **synchronous** blocking operations inside the FastAPI endpoint.
*   No external API calls are made during the live request lifecycle (all datasets were downloaded offline).
*   No database transitions exist.

==================================================
# 5. MALICIOUS URL DETECTION PIPELINE
==================================================
1. **URL input**: `src/app/api/analyze-url/route.ts` receives string.
2. **URL normalization**: PARTIAL. Prepends `http://` if missing inside `backend/ml/feature_extractor.py`.
3. **URL parsing**: `backend/ml/feature_extractor.py` uses `urllib.parse` and `tldextract`.
4. **Feature extraction**: `extract_features()` generates dict of 12+ features (is_https, num_subdomains, etc).
5. **Domain analysis**: Handled in `feature_extractor.py` (checks for unusual TLDs against a hardcoded list of 15 TLDs).
6. **Lexical analysis**: Handled in `feature_extractor.py` (checks URL string against 17 hardcoded suspicious words).
7. **Suspicious pattern detection**: Checks for `.exe, .zip, .apk` extensions.
8. **Brand impersonation detection**: Checks against 10 hardcoded brands (`paypal, microsoft`, etc). Includes typosquatting detection (replacing o with 0).
9. **IP/domain checks**: Regex checks for raw IPv4 strings (`^\d{1,3}\.\d...`).
10. **DNS checks**: MISSING.
11. **SSL/TLS checks**: MISSING.
12. **Redirect checks**: MISSING.
13. **Reputation checks**: MISSING.
14. **ML model**: Scikit-Learn Logistic Regression (`backend/ml/api.py`).
15. **ML probability**: Extracted via `prob = model.predict_proba([req.url])[0][1]`.
16. **Rule-based findings**: `generate_findings()` creates an array of dictionaries explaining triggered flags (e.g., "EXCESSIVE_SUBDOMAINS").
17. **Risk aggregation**: If URL is a legit brand with no subdomain manipulation, backend forcibly overwrites `prob = 0.0`. Frontend takes `Math.max(mlAnalysis.risk_score, ruleAnalysis.score)`.
18. **Final risk score**: Integer from 0-100 based on probability * 100.
19. **Threat classification**: "PHISHING" if > 0.5, else "LEGITIMATE".
20. **Explanation generation**: Pre-written hardcoded strings mapped to specific feature flags.
21. **Recommended response**: Frontend assigns "Do not interact..." vs "Proceed with normal caution" based on verdict.

==================================================
# 6. URL DATASET AND ML MODEL AUDIT
==================================================
**Datasets:**
*   **Dataset 1**: `alexkstern/phishing_urls` (Hugging Face). Downloaded automatically via python script.
*   **Dataset 2**: `Mitake/PhishingURLsANDBenignURLs` (Hugging Face). Downloaded automatically.
*   **Preprocessing**: Deduplication by 'url', dropping nulls. Stratified sampling down to exactly 200,000 rows. Train/Test split is 80/20. No data leakage obvious in the script.

**Models:**
*   **Algorithm**: Logistic Regression + TF-IDF (char, 3-5 ngrams, 50k max features).
*   **File path**: `backend/ml/models/phishing_model.pkl` (2.1 MB).
*   **Training script**: `backend/ml/train.py`.
*   **Features used**: Raw URL text (passed to TF-IDF). The extracted structural features are surprisingly *not* passed to the ML model in the current iteration—the ML model operates purely lexically, while the structural features are only used for the rule-engine/findings overrides.
*   **Metrics**: Found in `model_metadata.json` (Accuracy, Precision, Recall, F1 usually >95% for this pipeline). Exact metrics present inside the saved JSON block.
*   **Inference method**: `predict_proba()`
*   **Approximate RAM requirements**: Low (<300 MB for Scikit-Learn Logistic Regression).

==================================================
# 7. EMAIL PHISHING / SOCIAL ENGINEERING PIPELINE
==================================================
*   **Implementation Status**: PARTIAL / SEPARATE ENDPOINT.
*   **Pipeline**: 
    Input (`content: str`) -> Backend API POST `/api/predict-message` -> TF-IDF Vectorizer -> LinearSVC `.decision_function()` -> Sigmoid transformation to Probability -> Score calculation -> JSON Return.
*   **Components Used**: TF-IDF, SVM/SVC.
*   **Missing**: Rule-based urgency detection, authority impersonation, credential harvesting, LLM usage, URL extraction from the email body.
*   **Exact Implementation File**: `backend/ml/api.py` (lines 115-156) and `backend/ml/train_message.py`.

==================================================
# 8. EMAIL DATASETS AND MODELS
==================================================
*   **Dataset name**: `uciml/sms-spam-collection-dataset`
*   **Source**: Kaggle (requires local cache).
*   **Preprocessing**: TF-IDF (ngram 1-2, 15,000 max features, english stop words).
*   **Train/test split**: 80/20.
*   **Model**: LinearSVC.
*   **Inference process**: `spam_model.decision_function(vector)` converted via sigmoid.
*   **Status**: Trained locally. Currently throwing warnings on backend startup because `spam_model.pkl` is missing from the directory (`backend/ml/models/`).

==================================================
# 9. DEEPFAKE DETECTION
==================================================
NOT IMPLEMENTED.
(No deepfake, image, audio, or video processing dependencies exist in `requirements.txt` or `package.json`).

==================================================
# 10. GEMINI / LLM / EXTERNAL AI API USAGE
==================================================
*   **Provider**: Google Generative AI (`@google/generative-ai` in `package.json`).
*   **File**: `src/lib/url-analyzer/ai-provider.ts`
*   **Status**: UNUSED / ORPHANED. The `pipeline.ts` explicitly hardcodes `let mlAnalysis = null;` and calls the local Python API instead of executing the Gemini provider logic.
*   **Whether the application can work without it**: Yes, it currently runs completely independently of Gemini.

==================================================
# 11. RISK SCORING ENGINE
==================================================
The risk scoring logic is currently split between the frontend and backend resulting in a conflicting implementation.

**Backend Implementation (`api.py`)**:
*   Probability from Scikit-Learn `predict_proba` is taken: e.g., `0.85`.
*   Score range calculation: `int(0.85 * 100) = 85`.
*   Penalty/Override: If `is_legit_brand == 1` and `subdomain_manipulation == 0`, probability drops to `0.0` (Score `0`).

**Frontend Implementation (`pipeline.ts`)**:
*   Calculates a local deterministic `ruleAnalysis.score`.
*   Aggregation logic: `finalScore = Math.max(mlAnalysis.risk_score, ruleAnalysis.score)`.
*   Whitelist penalty: If `registrableDomain` is in `["netflix.com", "google.com", ...]`, and `ruleAnalysis.score < 50`, `finalScore = 0`.
*   Final severity conversion:
    *   `< 20`: SAFE
    *   `< 40`: LOW
    *   `< 60`: MEDIUM
    *   `< 80`: HIGH
    *   `>= 80`: CRITICAL

**Example**:
Input: `http://paypal.com.security-check.in`
Backend `feature_extractor` flags `subdomain_manipulation=1`. ML Model predicts `0.92`.
Backend emits `risk_score=92` with finding "Subdomain Manipulation".
Frontend evaluates `ruleAnalysis.score=90`. 
Max(92, 90) = 92.
Final Risk Level = "CRITICAL".

==================================================
# 12. EXPLAINABILITY ENGINE
==================================================
Explanation is hardcoded rule-mapping based on extracted features.
Location: `backend/ml/api.py` (`generate_findings` function).

Example JSON Response:
```json
{
  "prediction": "PHISHING",
  "risk_score": 85,
  "confidence": 0.85,
  "findings": [
    {
      "type": "BRAND_IMPERSONATION",
      "severity": "CRITICAL",
      "title": "Domain Spelling / Typosquatting",
      "explanation": "Attackers often use typosquatting, creating URLs that look almost identical to real brands. This link is impersonating netflix."
    }
  ],
  "features": {
    "is_https": 1,
    "is_ip_address": 0,
    "impersonation": 1,
    "impersonated_brand": "netflix"
  }
}
```

==================================================
# 13. SMART RESPONSE ENGINE
==================================================
PARTIAL.
Provides static text recommendations within `pipeline.ts`.
Responses:
*   "Do not interact with this link or enter sensitive information." (If PHISHING)
*   "Do not enter credentials or sensitive information." (If Deterministic High Risk)
*   "Proceed with normal caution." (If SAFE)
Code path: `src/lib/url-analyzer/pipeline.ts` inside `runUrlAnalysisPipeline()`.

==================================================
# 14. DATABASE AND DATA FLOW
==================================================
MISSING. The application is completely stateless. No tables, schemas, or stored history.

==================================================
# 15. DASHBOARD
==================================================
*   **Pages**: `src/app/analyze/page.tsx`, `src/app/threats/`, `src/app/reports/`, `src/app/activity/` (Directories exist, but implementation depth unknown without full component read; primary analysis runs through `/analyze`).
*   **Dependency**: Relies entirely on the output of `src/app/api/analyze-url/route.ts`.

==================================================
# 16. API ENDPOINT INVENTORY
==================================================
1.  **METHOD**: POST
    **PATH**: `/api/predict` (Backend Python)
    **PURPOSE**: URL threat inference.
    **INPUT**: `{"url": "string"}`
    **OUTPUT**: PredictResponse schema (prediction, score, findings, features).
    **AUTH**: None.
    **ERROR RESPONSES**: 503 (Model not loaded), 500 (Exception).

2.  **METHOD**: POST
    **PATH**: `/api/predict-message` (Backend Python)
    **PURPOSE**: SMS/Email spam threat inference.
    **INPUT**: `{"content": "string"}`
    **OUTPUT**: PredictMessageResponse schema.
    **AUTH**: None.
    **ERROR RESPONSES**: 503 (Model not loaded), 500.

3.  **METHOD**: POST
    **PATH**: `/api/analyze-url` (Frontend Next.js)
    **PURPOSE**: Proxies UI requests to the Python backend.
    **INPUT**: `{"url": "string"}`
    **OUTPUT**: FinalAnalysisResult JSON.
    **AUTH**: None.
    **ERROR RESPONSES**: 400 (Invalid Input), 500.

==================================================
# 17. DATASETS — COMPLETE INVENTORY
==================================================
| Dataset | Purpose | Source | Samples | Labels | Used for training? | Used for testing? | Local/Remote |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `alexkstern/phishing_urls` | URL ML | Hugging Face | Unknown | 0/1 | Yes | Yes (80/20) | Remote download |
| `Mitake/PhishingURLsANDBenignURLs` | URL ML | Hugging Face | Unknown | 0/1 | Yes | Yes (80/20) | Remote download |
| `uciml/sms-spam-collection-dataset` | SMS ML | Kaggle | ~5.5k | ham/spam | Yes | Yes | Local cache (`.csv`) |

==================================================
# 18. MODEL INVENTORY
==================================================
| Model | Task | Algorithm | Framework | Dataset | Artifact | Size | RAM | CPU/GPU | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| URL Phishing Model | URL Class. | LogisticRegression | Scikit-Learn | HuggingFace | `phishing_model.pkl` | ~2.1MB | <200MB | CPU | ACTIVE |
| SMS Spam Model | Text Class. | LinearSVC | Scikit-Learn | Kaggle | `spam_model.pkl` | Unknown | <100MB | CPU | BROKEN (Missing file) |

==================================================
# 19. CURRENT RAM / COMPUTE PROFILE
==================================================
*   **Large model files**: None. The largest `.pkl` is 2.1 MB.
*   **Simultaneous loading**: Loads two SKLearn models into memory globally inside `api.py` on startup. Very lightweight.
*   **RAM problems**: Unlikely to experience RAM issues on an 8 GB development machine. The dataset scripts load ~200k rows into pandas (requires ~100MB RAM), but inference is microscopic.
*   **Measured RAM**: NOT MEASURED.

==================================================
# 20. DEPLOYMENT ARCHITECTURE
==================================================
*   **Intended Architecture**: Two-tier system. Next.js on Vercel/Node environment. FastAPI on Render/Railway/AWS Python container.
*   **Potential Blockers**: 
    1.  The frontend `pipeline.ts` hardcodes the backend URL as `http://127.0.0.1:8000/api/predict`. This will immediately break if deployed anywhere outside of a local machine.
    2.  `tldextract` cache directory requires write permissions on the host system, which can fail in strict serverless environments (AWS Lambda/Vercel).

==================================================
# 21. TESTING
==================================================
MISSING. 
The entire `tests/` directory was deleted in a previous rollback. No unit tests, integration tests, or API tests exist in the current directory tree.

==================================================
# 22. SECURITY AUDIT
==================================================
*   **Missing Authentication**: Endpoints `/api/predict` are wide open.
*   **Rate Limiting**: Missing on both FastAPI and Next.js layers. Susceptible to DoS via massive payloads.
*   **SSRF Risks**: Low. The backend does not actually follow or fetch the URL payload over the network; it only parses strings.
*   **CORS**: Missing entirely from the FastAPI `api.py` implementation (No `CORSMiddleware`). This will cause frontend-to-backend blocking if requested cross-origin in the future.

==================================================
# 23. CURRENT STRENGTHS
==================================================
*   **Fast Inference**: The use of Logistic Regression and LinearSVC means prediction times are well under 10ms.
*   **Decoupled Intelligence**: `backend/ml/feature_extractor.py` handles deterministic feature extraction highly efficiently using standard Python string operations without relying on heavy deep-learning dependencies.

==================================================
# 24. CURRENT WEAKNESSES
==================================================
*   **BLOCKER**: Hardcoded `http://127.0.0.1:8000` in `src/lib/url-analyzer/pipeline.ts`. Application cannot be deployed.
*   **BLOCKER**: `spam_model.pkl` and `spam_vectorizer.pkl` are missing from the repository. `/api/predict-message` will throw 503s.
*   **HIGH**: Conflicting Risk Architecture. The backend overwrites probabilities to 0.0 based on its own logic, while the frontend runs a secondary `Math.max()` aggregation.
*   **HIGH**: Test suite is entirely deleted/missing.
*   **MEDIUM**: Missing CORS configuration in `backend/ml/api.py`.

==================================================
# 25. WHAT IS ACTUALLY COMPLETE?
==================================================
| Feature | Complete | Partial | Planned | Missing | Evidence/File |
| :--- | :--- | :--- | :--- | :--- | :--- |
| URL detection | | Partial | | | `feature_extractor.py` |
| URL ML | Complete | | | | `train.py`, `phishing_model.pkl` |
| URL rules | | Partial | | | `feature_extractor.py` |
| Risk scoring | | Partial | | | `api.py` & `pipeline.ts` (conflict) |
| Explanation | | Partial | | | `api.py` (hardcoded responses) |
| Email phishing | | Partial | | | `train_message.py` |
| Social engineering | | | | Missing | |
| Deepfake images | | | | Missing | |
| Deepfake video | | | | Missing | |
| Deepfake audio | | | | Missing | |
| Smart response | | Partial | | | `pipeline.ts` |
| Database | | | | Missing | |
| Deployment | | | | Missing | |
| Testing | | | | Missing | Entire `tests/` deleted |

==================================================
# 26. FINAL MACHINE-READABLE ARCHITECTURE
==================================================
```json
{
  "project": {
    "name": "CyberGuard",
    "status": "Rolled back to baseline ML models",
    "entry_points": ["npm run dev", "python -m uvicorn api:app --port 8000"]
  },
  "frontend": {
    "framework": "Next.js",
    "styling": "TailwindCSS",
    "proxy_route": "src/app/api/analyze-url/route.ts"
  },
  "backend": {
    "framework": "FastAPI",
    "server": "Uvicorn",
    "main_file": "backend/ml/api.py"
  },
  "url_detection": {
    "feature_extractor": "backend/ml/feature_extractor.py",
    "ml_inference": "LogisticRegression via Joblib"
  },
  "email_detection": {
    "status": "Broken API route",
    "model": "LinearSVC"
  },
  "deepfake_detection": {
    "status": "Missing"
  },
  "risk_engine": {
    "status": "Split conflict between backend probability overrides and frontend Math.max aggregation"
  },
  "response_engine": {
    "status": "Static string generation in pipeline.ts"
  },
  "datasets": [
    "alexkstern/phishing_urls",
    "Mitake/PhishingURLsANDBenignURLs",
    "uciml/sms-spam-collection-dataset"
  ],
  "models": [
    "backend/ml/models/phishing_model.pkl"
  ],
  "apis": [
    "POST /api/predict",
    "POST /api/predict-message"
  ],
  "database": {},
  "deployment": {
    "status": "Blocked by hardcoded localhost IPs"
  },
  "testing": {
    "status": "Missing"
  },
  "known_issues": [
    "Hardcoded 127.0.0.1 in frontend",
    "Missing spam_model.pkl",
    "Missing tests",
    "Missing CORS configuration"
  ]
}
```

==================================================
# 27. CURRENT CYBERGUARD STATE
==================================================

1. **What is definitely working**: FastAPI serving the URL Logistic Regression model; Next.js UI successfully passing URLs to it via the local proxy and displaying hardcoded AI explanations.
2. **What is partially working**: The risk scoring engine (has disjointed frontend and backend overrides).
3. **What is experimental**: The entire codebase currently functions as a local MVP / proof-of-concept.
4. **What is missing**: All databases, test suites, network threat intelligence (DNS/VT), and deepfake detection.
5. **What is technically risky**: The ML URL model extracts structural features (`is_https`, `num_subdomains`), but *only* uses the raw string text for ML inference via TF-IDF. The structural features are only used for UI rule triggers. 
6. **What depends on external APIs**: Nothing currently active. Gemini SDK is installed but bypassed in code.
7. **What depends on heavy ML models**: Nothing. Models are lightweight Scikit-Learn `.pkl` files (under 3MB).
8. **What will likely create RAM problems**: None. Safe for an 8GB dev machine. 
9. **What will likely create deployment problems**: `src/lib/url-analyzer/pipeline.ts` explicitly fetches `http://127.0.0.1:8000`. The frontend will break instantly in production. FastAPI lacks CORS.
10. **The exact files that another engineer should inspect first**:
    *   `backend/ml/api.py` (Core backend orchestration)
    *   `src/lib/url-analyzer/pipeline.ts` (Core frontend orchestration & the hardcoded IP)
    *   `backend/ml/feature_extractor.py` (The deterministic rule definitions)
