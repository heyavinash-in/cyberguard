# CyberGuard Message Detection Engine v1

## 1. Architecture
The Message Detection Engine acts as a centralized backend subsystem to analyze SMS, email, and raw text for phishing, spam, and social-engineering threats. It relies on a deterministic processing pipeline augmented by Machine Learning (TF-IDF Ensemble).

**Workflow:**
1. Text is preprocessed (normalized, tokens generated for URLs/emails).
2. Word-level and Character-level TF-IDF pipelines score the message.
3. A Deterministic Rule Engine scans for categorized social engineering tactics (e.g., Urgency, Threat, Credential Harvesting).
4. Extracted URLs are routed to the *CyberGuard URL Detection Engine* to leverage deep structural URL analysis.
5. Evidence is fused into the *Central Risk Engine* without double-counting (e.g., "Account blocked" + "Verify immediately" consolidates into `URGENCY_THREAT` and `CREDENTIAL_HARVESTING`).
6. A bounded 0-100 risk score, severity, and deterministic recommendations are returned to the frontend.

## 2. Dataset
The engine currently trains on the **UCI SMS Spam Collection** (available locally and via KaggleHub/HuggingFace).
- **Training Samples:** 4,135
- **Validation Samples:** 1,034
- **Classes:** Benign (Ham), Phishing/Spam (Spam)

## 3. Preprocessing
Text is standardized to lowercase, and specific IOCs (URLs, Email addresses, Phone numbers) are replaced with specific placeholders (`URL_TOKEN`, `EMAIL_TOKEN`) to allow the model to recognize their presence contextually without overfitting to specific domain names.

## 4. ML Models
The MVP uses a Scikit-Learn `VotingClassifier` (Soft Voting) built on top of:
- **Model A:** `TfidfVectorizer(analyzer='word')` + `LogisticRegression`
- **Model B:** `TfidfVectorizer(analyzer='char', ngram_range=(3,5))` + `LogisticRegression`

This enables the model to detect both known spam terminology and adversarial structural evasions (e.g., `v3r1fy`).

## 5. Social-Engineering Rules
Regex-based dictionaries map strings to specific adversarial behaviors:
- `URGENCY_PRESSURE`: "act now", "expires today"
- `THREAT_OR_CONSEQUENCE`: "account suspended", "legal action"
- `CREDENTIAL_REQUEST`: "verify account", "password"
- `FINANCIAL_LURE`: "send money", "invoice"
- `AUTHORITY_IMPERSONATION`: "Microsoft", "Tax Department"

## 6. URL Integration
URLs are extracted using a greedy regex stripped of trailing punctuation, then fed directly into `evaluate_risk()` from the existing `URL Detection Engine`. URL severity heavily influences (but does not unboundedly inflate) the final message score.

## 7. Risk Fusion
Final risk is evaluated by:
- Taking the `ML_SIGNAL` (up to 45 pts).
- Applying contextual multipliers (e.g., Mentioning "Bank" is 10 points. Mentioning "Bank" + asking for "OTP" becomes 50 points).
- Extracting the maximum URL penalty (up to 70 pts).
- Capping at 100.

## 8. Explainability
Every score > 20 is accompanied by a structured `Finding` array. The model produces evidence blocks indicating *why* the message was penalized (e.g., highlighting `URGENCY_THREAT` due to matching "verify immediately").

## 9. API
`POST /api/analyze/message`
Returns a strict JSON format with Classification, Risk Score, Severity, Confidence, ML output, extracted URLs, Findings, and Recommended Responses.

## 10. Training & Evaluation
Execution: `python backend/app/ml/train_message_model.py`
Evaluation is run automatically against the 20% validation split.

## 11. Limitations (Honest Assessment)
- **Dataset Bias:** Trained on SMS spam. It struggles with long-form, highly conversational phishing typical in modern Business Email Compromise (BEC).
- **False Positives:** Mentioning "Netflix" and "Payment" in legitimate billing texts may trigger `FINANCIAL_LURE` + `AUTHORITY_IMPERSONATION`.
- **Adversarial Evasion:** Heavy Unicode obfuscation or extreme spacing (e.g. `p a s s w o r d`) can bypass deterministic rules.
- **No SSRF:** URLs are structurally evaluated but *not* visited. Advanced dynamic payloads are invisible to v1.
- **Prototype Status:** v1 is a hackathon-ready heuristic engine, not an enterprise zero-day defense tool.

## 12. Future Improvements
- Train on a dedicated phishing email dataset (e.g., Enron Phishing Corpus).
- Integrate Gemini interactions purely for *explanation generation* of the detected deterministic evidence.
- Employ a lightweight local Transformer (`distilbert`) instead of TF-IDF for contextual understanding.
