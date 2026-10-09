import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

questions = [
    # Category 1: System Architecture & Tech Stack
    ("1. What is the overall architecture of CyberGuard?", "CyberGuard uses a decoupled microservices architecture with a Next.js (React) frontend for the UI and a FastAPI (Python) backend for the ML inference and heuristic rule engine."),
    ("2. Why did you choose Next.js for the frontend?", "Next.js provides excellent performance, Server-Side Rendering (SSR) capabilities, and a great developer experience with Tailwind CSS integration, making it ideal for a modern, responsive security dashboard."),
    ("3. Why did you choose FastAPI for the backend instead of Flask or Django?", "FastAPI is extremely fast, inherently asynchronous, and automatically generates API documentation. It is specifically designed to handle ML model serving efficiently."),
    ("4. How do the frontend and backend communicate?", "They communicate via asynchronous RESTful HTTP POST requests. The Next.js frontend sends JSON payloads containing the URL or message to the FastAPI endpoints, which return the analysis results."),
    ("5. Where is the ML model hosted?", "The ML model is hosted locally on the FastAPI server and loaded into memory on server startup to ensure ultra-low latency predictions without relying on third-party cloud ML APIs."),
    ("6. How did you handle CORS (Cross-Origin Resource Sharing) between the frontend and backend?", "Since both run locally during development (frontend on port 3000, backend on 8000), FastAPI's CORSMiddleware is configured to allow requests from the Next.js origin."),
    ("7. Is the application stateful or stateless?", "The FastAPI backend is stateless, making it highly scalable. The Next.js frontend manages the state (loading, results, errors) locally on the client side using React hooks."),
    ("8. How is the codebase structured?", "The project is divided into a 'src' directory for the Next.js frontend and a 'backend/ml' directory for the Python FastAPI server, ML training scripts, and pickled models."),
    ("9. What would it take to deploy this architecture to the cloud?", "We could containerize the backend using Docker and deploy it to AWS ECS or Google Cloud Run, while the Next.js frontend could be deployed to Vercel or Netlify."),
    ("10. How do you handle error states and API failures?", "The frontend wraps API calls in try-catch blocks and checks for 'success' flags in the JSON response. If the backend is down or throws an error, the UI elegantly displays a fallback error message without crashing."),

    # Category 2: Machine Learning Pipeline
    ("11. What machine learning model are you using for URL detection?", "We are using a Logistic Regression classifier combined with a TF-IDF (Term Frequency-Inverse Document Frequency) Vectorizer, packaged as a Scikit-Learn Pipeline."),
    ("12. Why Logistic Regression and not a Deep Neural Network?", "Logistic regression is highly interpretable, extremely fast to train and serve, and performs exceptionally well on text classification tasks like URL analysis when paired with TF-IDF. Deep learning would be overkill and slower."),
    ("13. What does TF-IDF do in this context?", "TF-IDF converts the raw URL string into a numerical matrix, giving higher mathematical weight to character combinations (n-grams) that frequently appear in phishing URLs but rarely in benign ones."),
    ("14. Did you use character n-grams or word n-grams?", "We used character n-grams. URLs don't have natural spaces, so analyzing character sequences (e.g., 'login', '.php') is much more effective than relying on standard word boundaries."),
    ("15. What were your model's final performance metrics?", "The model achieved an Accuracy of 96.11%, Precision of 95.87%, Recall of 90.81%, and an F1 Score of 93.27%."),
    ("16. Why is Precision particularly important for this project?", "High precision means fewer false positives. If the system constantly blocks legitimate websites, users will stop trusting it. 95.87% precision ensures that when it flags a threat, it is almost certainly a threat."),
    ("17. What is an F1 Score and why did you track it?", "The F1 Score is the harmonic mean of precision and recall. It gives us a balanced metric to ensure the model isn't just predicting 'safe' for everything in an imbalanced dataset."),
    ("18. How long does the model take to predict a single URL?", "Because it is a linear model and loaded into RAM on startup, inference takes a fraction of a millisecond, allowing for real-time scanning."),
    ("19. How did you save and load the trained model?", "We used Python's 'joblib' library to serialize (pickle) the Scikit-Learn Pipeline into a .pkl file, which the FastAPI server deserializes upon startup."),
    ("20. How would you handle model drift over time?", "We would periodically scrape new phishing URLs from databases like PhishTank, combine them with our dataset, and run the automated train.py script to retrain and redeploy the model."),

    # Category 3: Dataset Selection & Data Preprocessing
    ("21. Where did you get the training data?", "We dynamically pulled datasets directly from the Hugging Face Datasets hub, specifically 'alexkstern/phishing_urls' and 'Mitake/PhishingURLsANDBenignURLs'."),
    ("22. Why did you combine two datasets?", "Combining datasets provided a massive, diverse sample size of over 1.3 million raw URLs, preventing the model from overfitting to the specific structure of just one dataset."),
    ("23. How did you handle duplicate data across the two datasets?", "We loaded them into Pandas DataFrames, concatenated them, and used drop_duplicates(subset=['url']) to ensure the model didn't train on redundant data."),
    ("24. How many rows did you actually train on?", "After deduplication and cleaning, we had over 868,000 unique URLs. We sampled the data to balance training speed with accuracy."),
    ("25. How did you handle missing values or nulls?", "We used Pandas dropna() to strip out any rows where the URL or the label was missing, ensuring a clean dataset."),
    ("26. What was the ratio of benign to phishing URLs?", "The datasets are generally balanced, but we ensured stratified splitting during train_test_split to maintain a representative ratio in both the training and testing sets."),
    ("27. Did you manually label any of the data?", "No, the Hugging Face datasets came pre-labeled by cybersecurity researchers, which allowed us to focus on pipeline engineering rather than manual data entry."),
    ("28. Did you pre-process the URLs before feeding them to the vectorizer?", "We ensured all URLs were treated as raw strings, allowing the TF-IDF character n-gram analyzer to natively detect structural anomalies without mutating the original text."),
    ("29. What issues did you face with PyArrow arrays from Hugging Face?", "When converting to Pandas, Scikit-Learn sometimes threw errors on PyArrow extension types. We ensured proper casting to standard numpy types before training."),
    ("30. How do you plan to update the dataset in the future?", "The training script is designed to programmatically fetch the latest data from Hugging Face, so updating the model simply requires re-running the script."),

    # Category 4: Feature Engineering & Deterministic Rules
    ("31. Why do you use deterministic rules in addition to the ML model?", "While ML is great at pattern recognition, deterministic rules allow us to catch known, absolute threats (like IP address routing) and provide specific, actionable explanations to the user."),
    ("32. How do you detect Brand Impersonation / Typosquatting?", "We strip hyphens from the domain and check if a known brand (like Netflix or PayPal) is hidden within the string, and we also check for common character swaps (like replacing 'o' with '0')."),
    ("33. What is Subdomain Manipulation?", "It's when attackers put a brand name in a subdomain to trick users, like 'paypal.com.login.xyz'. Our system uses tldextract to isolate the true root domain and flag this tactic."),
    ("34. Why do you flag URL shorteners like Bitly?", "URL shorteners hide the final destination of a link. While not inherently malicious, they are heavily abused in phishing, so we flag them as 'Medium Risk' to urge user caution."),
    ("35. How does the system handle legitimate brand URLs like paypal.com?", "We built an explicit whitelist for top legitimate brands. If the root domain matches the brand exactly, it forces the threat score to 0, completely overriding any false positives from the ML model."),
    ("36. What happens if a link triggers an automatic download?", "The feature extractor parses the URL path. If it ends in an executable extension like .exe, .zip, or .bat, it immediately flags it as a 'High' Direct Download threat."),
    ("37. How do you detect unusual Top-Level Domains (TLDs)?", "We maintain a list of historically cheap and frequently abused TLDs (like .xyz, .top, .cc). If the URL uses one, we alert the user."),
    ("38. Why is an IP address in a URL considered dangerous?", "Legitimate websites almost always use registered domain names. URLs that route directly to raw IP addresses are a classic technique used to hide the identity of phishing servers."),
    ("39. Does the system check for HTTPS?", "Yes, it parses the scheme. If the URL uses unencrypted HTTP, it triggers a low-severity warning, as modern secure sites mandate HTTPS."),
    ("40. How does the deterministic score interact with the ML score?", "The pipeline takes the maximum of the two scores, ensuring that if either the ML model or the strict rules detect a critical threat, the user is protected."),

    # Category 5: Explainable AI (XAI) & Interpretability
    ("41. What is Explainable AI (XAI)?", "XAI refers to methods that allow humans to understand the reasoning behind a machine learning model's predictions, rather than treating the model as a 'black box'."),
    ("42. Did you implement XAI in CyberGuard?", "Initially yes. We extracted the coefficients from the Logistic Regression model and multiplied them by the URL's TF-IDF matrix to find exactly which n-grams caused a 'Phishing' prediction."),
    ("43. Why did you ultimately remove the NLP XAI output from the UI?", "Because it relied on character n-grams, the XAI would output fragmented strings (like 'pay', 'payp', 'aypal'). While mathematically accurate, it confused users, so we opted for heuristic-based explanations instead."),
    ("44. How do you explain the threat to the user now?", "We map the deterministic features (like impersonation, unusual TLDs, downloads) to human-readable explanations on the frontend, giving users clear, understandable reasons."),
    ("45. Why is explainability important in cybersecurity?", "Users and security analysts need to trust the tool. If a tool just says 'Threat: 99' with no context, the user might ignore it. If it says 'Threat: 99 because it impersonates Netflix and downloads a .exe', they take action."),
    ("46. Could you implement XAI for word-level models?", "Yes, if we trained a word-level TF-IDF model, the XAI would output full words (like 'login' or 'free'), which would be much more readable, though word-level models often miss obfuscated URLs."),
    ("47. How does the frontend handle these explanations?", "The FastAPI backend returns an array of 'findings' (JSON objects with titles and explanations), which the Next.js frontend maps directly into a bulleted list in the UI."),
    ("48. Does the AI provide a recommendation?", "Yes, the pipeline dynamically generates a recommendation (e.g., 'Do not interact with this link') based on the final calculated risk score."),
    ("49. What happens if the ML model is unavailable?", "The backend gracefully falls back to the deterministic rule engine. The UI indicates 'AI_ENGINE: INACTIVE' but still provides a baseline security analysis."),
    ("50. Can the user see the exact threat score?", "Yes, the Next.js UI features a large, dynamic 0-100 threat score meter with color coding (Green/Safe, Yellow/Suspicious, Red/Critical) for immediate visual feedback."),

    # Category 6: Security & Performance
    ("51. How fast is the URL analysis?", "Because the model is loaded into RAM and the rules are evaluated using fast string manipulation, the entire backend analysis takes single-digit milliseconds."),
    ("52. Is user data stored or logged?", "In this current iteration, the backend operates entirely in memory and does not log user queries to a database, ensuring complete privacy for the URLs being scanned."),
    ("53. What happens if a user submits a massive string to crash the server?", "FastAPI and Uvicorn have built-in request size limits, and we can easily add Pydantic validators to cap the URL length to prevent buffer overflows or DoS attacks."),
    ("54. How do you prevent XSS (Cross-Site Scripting) in the frontend?", "Next.js and React inherently sanitize dynamic variables before rendering them to the DOM, preventing script injection from malicious URLs."),
    ("55. How do you handle clipboard API security constraints?", "Modern browsers block programmatic clipboard reading over non-HTTPS connections. We implemented try-catch blocks to degrade gracefully, prompting the user to paste manually instead of crashing."),
    ("56. What is the impact of using Uvicorn as the ASGI server?", "Uvicorn is lightning-fast and built on uvloop, allowing the FastAPI backend to handle thousands of concurrent analysis requests if deployed at scale."),
    ("57. Why didn't you use a heavy framework like Next.js API routes for the ML?", "Next.js runs on Node.js, which is poor for heavy computational ML tasks. Separating the ML into a Python FastAPI backend ensures optimal performance and access to the Scikit-Learn ecosystem."),
    ("58. Is the application vulnerable to prompt injection?", "No, because we are using deterministic ML classifiers (Logistic Regression) rather than generative LLMs, the model cannot be 'tricked' via prompt injection-it only does mathematical classification."),
    ("59. How do you handle network latency between frontend and backend?", "We keep the JSON payloads extremely small, and the frontend uses loading spinners and React state to ensure the user knows the request is processing."),
    ("60. What would you do to secure the API in production?", "We would add rate limiting, require API keys or JWT authentication, and deploy it behind a Web Application Firewall (WAF) and HTTPS reverse proxy (like Nginx)."),

    # Category 7: Frontend Integration & UI/UX
    ("61. How did you design the user interface?", "We used Tailwind CSS for rapid, utility-first styling, aiming for a modern, 'cybersecurity' aesthetic with dark themes, glass-morphism effects, and color-coded threat indicators."),
    ("62. What do the different colors signify?", "Emerald Green (0-39) means safe, Amber Yellow (40-74) means suspicious, and Red (75-100) indicates a critical threat."),
    ("63. How does the frontend handle loading states?", "We use React's 'useState' to toggle a loading boolean. When true, the scan button disables and shows a spinning radar icon to prevent duplicate submissions."),
    ("64. Why did you include example buttons?", "Example buttons ('malicious-phish.xyz', 'benign-repo.git') improve UX by allowing users to instantly test the tool's capabilities without having to hunt for URLs themselves."),
    ("65. How is the Next.js routing structured?", "We used the Next.js App Router, with separate routes for URL scanning (/analyze/url), message analysis (/analyze/message), and the main dashboard."),
    ("66. What are Lucide-React icons used for?", "We use them to add lightweight, scalable vector icons (like shields, radars, and alerts) to the UI to quickly convey status and improve visual hierarchy."),
    ("67. Is the application mobile responsive?", "Yes, by utilizing Tailwind's responsive prefixes (like 'md:' and 'lg:'), the grid layouts and inputs stack elegantly on smaller mobile screens."),
    ("68. How did you handle client-side rendering?", "We used the 'use client' directive at the top of the page files, as the dashboard relies heavily on browser APIs (clipboard) and interactive React hooks."),
    ("69. What happens if the backend sends an unexpected response format?", "The frontend has fallback logic (e.g., `result.risk ?? 0`) and try-catch error states to ensure the UI remains stable even if the API contract breaks."),
    ("70. How do you pass data between pages?", "Currently, the state is managed locally within the page components. We can also use URL search parameters (e.g., ?q=...) to pre-fill the input fields if navigating from the dashboard."),

    # Category 8: Challenges & Overcoming Roadblocks
    ("71. What was the hardest part of building the ML pipeline?", "Tuning the vectorizer. Moving from manual feature arrays to a full TF-IDF text pipeline required completely restructuring how the FastAPI server processed inputs."),
    ("72. How did you solve the false positive issue with PayPal?", "The ML model learned that the word 'paypal' meant phishing due to the dataset skew. We solved this by implementing an explicit brand whitelist in the heuristic extractor to override the ML score for legitimate domains."),
    ("73. Why did Next.js crash when clicking the paste button?", "It threw a 'NotAllowedError' because browsers block clipboard access over local HTTP connections. We wrapped it in a try-catch to log a warning instead of crashing the React tree."),
    ("74. How did you handle the PyArrow TypeError during dataset loading?", "The Hugging Face datasets returned PyArrow arrays, which train_test_split couldn't index. We explicitly cast the datasets to Pandas DataFrames to ensure compatibility with Scikit-Learn."),
    ("75. Why did you abandon the first XGBoost model?", "While powerful, the XGBoost model relied on handcrafted numerical features and achieved 89% accuracy. Switching to a TF-IDF text pipeline with Logistic Regression bumped accuracy to 96% and reduced complexity."),
    ("76. What was a major challenge with the UI?", "Mapping the backend JSON response correctly to the React state. We had to write mapping logic to pull out the 'title' and 'explanation' fields from the nested 'riskFactors' array."),
    ("77. How did you handle brand impersonation logic?", "Initially, we just checked if the brand was in the domain, but that missed obfuscated URLs like 'net-flix'. We improved it by stripping hyphens before doing the substring check."),
    ("78. Did you have any port conflicts during development?", "Yes, port 3000 was occasionally locked by lingering Node processes. We had to use taskkill commands to free the port before booting the Next.js server."),
    ("79. How do you handle URLs that don't have 'http://'?", "The URLFeatureExtractor checks if the string starts with 'http'. If not, it automatically prepends 'http://' so the python 'urlparse' library can correctly identify the hostname and path."),
    ("80. What was the most satisfying bug to fix?", "Deploying the brand whitelist. Seeing 'paypal.com' drop from a 99/100 Critical Threat down to a 0/100 Safe score proved that our hybrid ML + Heuristic approach was working perfectly."),

    # Category 9: Future Scalability & Feature Roadmap
    ("81. How could you improve the ML model further?", "We could experiment with deep learning models like LSTMs or Transformers (BERT) for sequence classification, though it would increase latency and computational cost."),
    ("82. What additional features could you add to the URL scanner?", "We could integrate live WHOIS lookups to check domain age (phishing domains are usually brand new) or integrate Google Safe Browsing APIs for secondary verification."),
    ("83. How would you handle scaling to 10,000 requests per second?", "We would deploy multiple instances of the FastAPI backend behind an Nginx load balancer and use a caching layer like Redis to instantly return results for recently scanned URLs."),
    ("84. Can this analyze files or attachments?", "Not currently. A future roadmap feature would be allowing users to upload .exe or .pdf files to be statically analyzed or hashed against VirusTotal databases."),
    ("85. How could you monetize or deploy this as a B2B service?", "We could offer a robust REST API for enterprises to integrate into their email servers or Slack workspaces, charging based on API request volume."),
    ("86. Will you add user accounts?", "Yes, we could use NextAuth or Firebase to let users create accounts, save their scan history, and receive weekly security reports."),
    ("87. Could you implement a browser extension?", "Absolutely. A Chrome extension could silently pass every visited URL to our FastAPI backend and throw an alert overlay if the risk score exceeds 80."),
    ("88. How can you improve the message scanner?", "By using advanced NLP sentiment analysis to detect urgency or threats, and Named Entity Recognition (NER) to flag when a message asks for sensitive entities like 'SSN' or 'Password'."),
    ("89. What is the plan for database integration?", "We would use PostgreSQL to log flagged threats for further model retraining, and MongoDB to store unstructured scan telemetry."),
    ("90. How will you keep the brand whitelist updated?", "We could maintain it in a database table or a remote configuration file, allowing admins to add new legitimate brands without redeploying the backend code."),

    # Category 10: Impact & Business Value
    ("91. What real-world problem does CyberGuard solve?", "Phishing and social engineering cost organizations billions annually. CyberGuard provides a free, instant, and explainable tool to verify if a link or message is a threat before the user clicks it."),
    ("92. Who is the target audience for this application?", "Everyday internet users who receive suspicious emails or texts, as well as IT administrators who need a quick triage tool for investigating employee reports."),
    ("93. How does this compare to existing tools like VirusTotal?", "VirusTotal relies heavily on aggregating third-party antivirus engine signatures. CyberGuard uses its own bespoke ML model specifically optimized for text-based structural anomaly detection in real-time."),
    ("94. Why is the 'Explanation' feature so valuable?", "Security awareness training relies on education. By explicitly telling the user *why* a link is bad (e.g., 'Subdomain manipulation'), CyberGuard trains the user to spot threats themselves in the future."),
    ("95. How does this project demonstrate Full-Stack capabilities?", "It integrates modern frontend engineering (React, Next.js, Tailwind), backend API design (FastAPI, Python), and Data Science (Scikit-Learn, NLP, Pandas) into one cohesive product."),
    ("96. What is the estimated cost to run this in production?", "Extremely low. Because the ML model is lightweight (not a massive LLM), it can run on basic CPU servers. AWS EC2 or DigitalOcean Droplets could host it for less than $10 a month."),
    ("97. How does the hybrid AI/Heuristic engine provide a business advantage?", "Pure ML models suffer from false positives, which angers users. Pure heuristic engines miss zero-day attacks. Combining them gives us high accuracy with fail-safe overrides."),
    ("98. Could this be used to protect internal company networks?", "Yes, it could be deployed entirely on-premise, allowing companies to scan sensitive internal emails without sending data out to cloud APIs."),
    ("99. How does CyberGuard handle user privacy?", "Because it doesn't log the URLs to a database and runs inference entirely in-memory, it guarantees complete privacy for the user's data."),
    ("100. What is the biggest takeaway from building this project?", "Bridging the gap between raw machine learning metrics and user experience. A 96% accurate model is useless if it flags standard brands or crashes the UI. True engineering requires robust error handling, explainability, and intelligent rule overrides.")
]

def generate_pdf():
    doc = SimpleDocTemplate("CyberGuard_Jury_QA.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        alignment=1, # Center
        spaceAfter=20
    )
    
    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        spaceAfter=6,
        leading=14
    )
    
    a_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        spaceAfter=14,
        leading=14,
        alignment=TA_LEFT
    )

    Story = []
    
    title = Paragraph("CyberGuard - 100 Jury Q&A", title_style)
    Story.append(title)
    
    for q, a in questions:
        q = q.replace('\u2014', '-').replace('\u2019', "'")
        a = a.replace('\u2014', '-').replace('\u2019', "'")
        
        p_q = Paragraph(q, q_style)
        p_a = Paragraph(a, a_style)
        
        Story.append(p_q)
        Story.append(p_a)
        
    doc.build(Story)
    print("ReportLab PDF generated successfully!")

if __name__ == '__main__':
    generate_pdf()
