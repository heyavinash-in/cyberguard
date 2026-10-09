This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

# CyberGuard Backend - Phase 2 (Security Feature Extraction)

CyberGuard's backend is a Python/FastAPI service utilizing a layered threat-intelligence architecture.

## Phase 2 Architecture
The backend analyzes URLs incrementally. Phase 1 ingests and safely normalizes a URL. Phase 2 (the current phase) acts as a **Security Feature Extraction** layer. It takes the normalized URL representation and deterministically extracts 60+ security signals without making any outbound requests.

## Feature Categories
The feature extractor generates structured signals in the following categories:
- **Structural:** Lengths, segment counts, special characters, hyphen ratios.
- **Domain:** IP address detection, private IPs, punycode, unusual TLDs.
- **Obfuscation:** Hexadecimal sequences, double slashes, credential embedding, percent encodings.
- **Brand:** Mismatches between recognizable brand keywords and the actual registrable domain.
- **Path:** Presence of suspicious authentication/payment keywords.
- **Query:** Detection of token leaks, open redirect parameters, and encoded payloads.
- **Complexity:** Entropy scores and digit-to-character ratios.
- **Subdomain:** Deep subdomains and subdomain impersonation.

## Important Note: Features are Signals, Not Verdicts!
The output of Phase 2 is **strictly deterministic signal extraction**. It does NOT produce a final risk score. None of these features on their own definitively prove a URL is malicious. Legitimate applications regularly use tokens, complex paths, or redirect parameters. These extracted features simply form the foundational input vector for downstream layers (like Machine Learning and Heuristics) which will calculate the final verdict.

## Examples of Brand-Domain Mismatch
Brand deception is a common phishing vector. CyberGuard parses URLs to identify exactly where a brand keyword appears:

1. **Legitimate Site:** \https://paypal.com/login   - Registrable Domain: \paypal.com   - \rand_matches_registrable_domain = true   - \possible_brand_domain_mismatch = false
2. **Subdomain Impersonation:** \https://paypal.example.com/login   - Registrable Domain: \example.com   - Subdomain: \paypal   - \rand_matches_registrable_domain = false   - \possible_brand_domain_mismatch = true
## Testing Instructions
The backend uses \pytest\ for automated test coverage. To execute the tests:

\\ash
# From the project root
python -m pytest tests/ -v
\This runs both Phase 1 Regression tests (normalization) and Phase 2 tests (feature extraction).

# CyberGuard Backend - Phase 3 (DNS / IP Intelligence)

Phase 3 extends the backend by adding controlled, deterministic DNS and network intelligence, keeping strict SSRF (Server-Side Request Forgery) boundaries.

## Phase 3 Architecture
The pipeline now conceptually flows as:
\URL Normalization\ -> \Security Feature Extraction\ -> \DNS/IP Intelligence\

CyberGuard performs:
- **A and AAAA Resolution:** Extracting IPv4 and IPv6 addresses.
- **CNAME Resolution:** Tracing canonical names for CDNs and aliases.
- **Reverse DNS (PTR):** Looking up hostnames for global IP addresses.
- **IP Classification:** Identifying if an IP is private, loopback, multicast, or link-local using Python's \ipaddress\ module.
- **TTL Extraction:** Collecting Time-to-Live metadata.

## Security and SSRF Boundary
During Phase 3, CyberGuard **does not** visit the submitted website.
- NO HTTP/HTTPS requests are made to the target.
- NO JavaScript is executed.
- NO arbitrary ports are scanned.
DNS resolution is the maximum network operation permitted at this layer, ensuring the analysis infrastructure remains safe from active exploitation.

## DNS Failure States
DNS is an external dependency and is inherently unreliable. Our resolver handles timeouts and SERVFAILs gracefully. DNS failures (like NXDOMAIN or timeout) are explicitly modeled in the \
esolution_status\ field. A missing PTR record or an NXDOMAIN does NOT inherently mean a domain is malicious.

## Testing Instructions
We use \pytest\ and \dnspython\ for asynchronous resolution.
The DNS layer is mocked in tests to ensure the test suite operates completely offline without depending on live public resolvers.

\\\ash
# From the project root
python -m pytest tests/ -v
\\\
This runs all 52+ tests across Phase 1, Phase 2, and Phase 3.


# CyberGuard Backend - Phase 5 (Heuristic Correlation & Explainable Rule Engine)

Phase 5 correlates signals from URL structure, security features, DNS intelligence, and external reputation to generate human-readable, deterministic heuristic findings.

## Phase 5 Architecture
`URL Normalization` -> `Security Feature Extraction` -> `DNS/IP Intelligence` -> `Reputation Intelligence` -> `Heuristic Correlation`

CyberGuard's heuristic engine consists of:
- **HeuristicContext:** An immutable object containing outputs from Phases 1-4.
- **Rule Registry:** A registry of `HeuristicRule` instances that evaluate the context independently.
- **Explainable Findings:** Rules produce deterministic `HeuristicFinding` objects with clear text explaining *why* the rule triggered.
- **Correlation:** Rules evaluate combinations of signals (e.g., brand deception + suspicious authentication path) to expose meaningful multi-faceted anomalies.

## Rule Categories
Phase 5 implements deterministic rules across 10 distinct categories:
1. `URL_STRUCTURE`: Long hostnames, deep subdomains, numeric-heavy patterns.
2. `BRAND_DECEPTION`: Brand mismatches in paths or subdomains.
3. `OBFUSCATION`: Percent encoding, suspicious double slashes.
4. `CREDENTIAL_DECEPTION`: Embedded usernames/passwords, especially with brand deception.
5. `REDIRECT_ABUSE`: Open redirect parameters combined with obfuscation or brand mismatch.
6. `DNS_INFRASTRUCTURE`: Resolution to private IPs, multiple global IPs, or failure.
7. `REPUTATION`: Exact matches from threat-intelligence sources.
8. `REPUTATION_CONFLICT`: Explicitly exposing provider disagreements (e.g., VirusTotal says clear, URLhaus says malware).
9. `NETWORK_ANOMALY`: Suspicious network indicators (link-local, multicast IPs).
10. `COMBINED_CORRELATION`: Meta-rules that trigger when multiple independent categories present anomalies simultaneously.

## Evidence Provenance
Each triggered rule explicitly records its `supporting_signals`. This creates an auditable, machine-readable evidence graph linking the final heuristic back to the exact feature or API result from Phases 1-4 that caused it. This is essential for the future explanation layer.

## Important False-Positive Safeguards
- The engine explicitly documents that certain indicators (e.g., URL encoding, DNS failure, missing provider records) are **NOT** automatically malicious.
- **No Verdict or Score:** Phase 5 provides explainable observations. It deliberately does *not* calculate a final numerical risk score or a probability of maliciousness.
- Provider disagreements are documented as `reputation_conflict` rather than automatically deciding which provider is correct.

## Testing Instructions
The test suite spans over 110 offline tests testing all phases, including comprehensive testing of heuristic combinations.

```bash
# From the project root
python -m pytest tests/ -v
```


# CyberGuard Backend - Phase 6 (Machine Learning Detection Engine)

Phase 6 implements a supervised Machine Learning layer using a hybrid feature space of character TF-IDF and structured Phase 2 URL heuristics.

## Phase 6 Architecture
`Phase 1 Normalization` + `Phase 2 Structured Features` -> `Hybrid Scikit-learn Pipeline` -> `Probability Output`

- **Important Separation**: The ML layer is strictly trained on structural/lexical features. It is explicitly **isolated** from Phase 3 (DNS), Phase 4 (Reputation), and Phase 5 (Heuristic Rules). This prevents data leakage where the model memorizes threat intelligence feeds rather than learning URL characteristics.
- **Explainability**: The model is based on Logistic Regression and Linear SVM baselines for transparency.
- **Group-Aware Validation**: Cross-validation uses `StratifiedGroupKFold` grouped by `registrable_domain` to prevent dataset leakage (e.g. testing `example.com/login` when `example.com/account` was in training).

## Feature Pipeline
1. **Lexical (Part A):** Character TF-IDF (3-gram to 5-gram) of the raw URL, designed to pick up on phishing keywords (login, verify, account, secure) and evasive syntax (xn--, %2F).
2. **Structured (Part B):** 50+ deterministic numerical/boolean features from Phase 2 (lengths, counts, entropy, brand match flags).
3. **Union:** Both feature sets are joined via `FeatureUnion` into a single, unified Scikit-learn Pipeline.

## Training Configuration
Configure training parameters in `.env` or `config.py`:
- `ML_DATASET_PATH` (default: `data/phishing_urls.csv`)
- `ML_URL_COLUMN`, `ML_LABEL_COLUMN`
- `ML_DECISION_THRESHOLD` (default: `0.50`)

To train a new model:
```bash
python -m backend.app.ml.train --dataset data/phishing_urls_small.csv --output models/url-phishing-v1
```

## Model Artifacts
Trained models are saved to `ML_MODEL_PATH` using `joblib`. 
- `model.joblib`: The full scikit-learn pipeline (preprocessing + classifier).
- `metadata.json`: Contains training timestamp, dataset fingerprint, threshold, evaluation metrics, ablation results, and the feature schema version.
- `error_analysis.json`: A dump of False Positives and False Negatives from the final untouched test set.

## Ablation Study
The training script natively performs an ablation study comparing:
- Lexical features only
- Structured Phase 2 features only
- Hybrid features
This proves the value of the engineered features.


# CyberGuard Backend - Phase 7 (Risk Aggregation & Final Assessment Engine)

Phase 7 introduces the deterministic evidence-fusion layer that aggregates signals from Phases 1-6 into a single, comprehensive `RiskAssessment`.

## Core Concepts
- **CyberGuard Risk Score**: An internal evidence index from 0–100. It is **NOT** a statistical probability of maliciousness.
- **Evidence Atomicity & Deduplication**: To prevent score inflation (e.g., getting +40 for a reputation match and another +20 for a heuristic built on that match), evidence is deduplicated via a suppression strategy.
- **Contribution Families & Caps**: Points are grouped by family (`ml`, `heuristics`, `reputation`, `dns`, `corroboration`). Each family has a configurable cap (e.g. `RISK_HEURISTIC_MAX_POINTS=30`) to prevent runaway additive scoring.
- **Known Threat Override**: Direct, verified threat intelligence matches automatically trigger a `known_threat` disposition, regardless of the numerical score.
- **Evidence Coverage & Quality**: If analysis layers fail (e.g. ML offline, reputation providers timeout), the URL is not silently marked benign. The `evidence_coverage` metric drops, producing an `insufficient_evidence` disposition if coverage is critically low.
- **Monotonicity**: Adding evidence of risk strictly increases or maintains the score, never decreases it. Provider conflicts (e.g. VirusTotal clean vs URLhaus malicious) are preserved—the positive evidence still contributes.

## Output Schema
The `/api/v1/url/analyze` response now includes a `risk` object:
```json
"risk": {
    "score": 82,
    "risk_level": "critical",
    "disposition": "known_threat",
    "assessment_quality": "high",
    "evidence_coverage": 100,
    "dominant_signals": [
        "Reputation match from urlhaus",
        "The ML model produced a phishing signal probability of 0.99"
    ],
    "contributions": [...],
    "suppressed_duplicates": [...],
    "policy_version": "risk-v1",
    "cap_info": {...}
}
```

## Configuration
Risk behavior is controlled entirely by `config.py` environment variables, including:
- `RISK_MAX_SCORE=100`
- `RISK_ML_MAX_POINTS=25`
- `RISK_HEURISTIC_MAX_POINTS=30`
- `RISK_REPUTATION_MAX_POINTS=45`
- `RISK_DNS_MAX_POINTS=10`
- `RISK_CORROBORATION_MAX_POINTS=10`

This layer relies purely on in-memory mapping and executes synchronously and rapidly.


