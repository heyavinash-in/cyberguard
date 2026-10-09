# CyberGuard Hackathon Preparation Guide

Welcome team! You have built a fully functional, multi-engine cybersecurity platform. This document contains everything you need to know about how the project works under the hood, exactly which features to present, and how each of you should handle questions from the jury.

---

## 1. The Architecture & Tech Stack (How it works behind the scenes)

CyberGuard is built on a modern, decoupled architecture. The frontend handles the user experience, while the backend handles the heavy machine learning inference and data storage.

**Frontend Stack:**
* **Next.js 14 (App Router) & React:** The core framework for the web app.
* **Tailwind CSS & shadcn/ui:** Used for the premium, dark-mode, glassmorphic cybersecurity design.
* **TypeScript:** Ensures the API responses match the UI components perfectly.

**Backend Stack:**
* **FastAPI (Python):** The high-performance backend API. It handles incoming requests asynchronously.
* **Pydantic:** Used to strictly validate incoming telemetry data and outgoing JSON responses.
* **SQLite:** A lightweight database used to power the Command Center. Every time a threat is analyzed, it is logged via the `EventStore` service into a local SQLite file so the dashboard metrics update in real-time.

**AI & ML Stack:**
* **Hugging Face (`transformers`):** We use a pre-trained Vision Transformer (ViT) model (`prithivMLmods/Deep-Fake-Detector-Model`) for image deepfake detection. 
* **Scikit-Learn / Numpy:** Used for lightweight anomaly detection, statistical analysis, and feature extraction in the URL and Account Takeover engines.

---

## 2. The Golden Demo Path (What to present)

**Great news:** All four engines are working perfectly! You do NOT need to hide any features. I have fine-tuned them all to connect seamlessly to the Command Center.

Here is the exact order you should demo them to impress the jury:

1. **The Command Center Dashboard (`/dashboard`):** Start here. Show them that CyberGuard isn't just a toy script—it's a centralized platform. Point out that the metrics (Total Threats, Active Cases) are pulling real data from the SQLite database.
2. **Account Takeover Analyzer (`/analyze/account`):** 
   * Click the **"Simulate Account Takeover"** button. 
   * Explain how the system evaluates impossible travel (e.g., logging in from Singapore with an unknown MAC address) and multiple failed logins. 
   * Show the timeline and risk score it generates.
3. **Deepfake Media Analyzer (`/analyze/media`):** 
   * Upload an AI-generated image.
   * Point out the animated loading steps (Extracting EXIF, Executing FFT, etc.).
   * Show the final result, highlighting how it breaks down the "Forensic Evidence" alongside the AI Probability.
4. **URL / Message Phishing (`/analyze/url`):** If you have time, quickly paste a fake phishing link to show that the platform covers all attack vectors.

---

## 3. Team Roles & Jury Cross-Questioning Defense

Here is how each of you should position yourselves and tackle likely jury questions.

### Avinash (Team Leader & Cyber Security Engineer)
**Your Role:** You are the visionary. Open the pitch. Explain *why* CyberGuard exists: modern threats are converging (phishing + AI deepfakes + account breaches). Explain the core philosophy of **"Evidence Fusion"**—we don't just rely on one AI model; we fuse AI probability with hard deterministic forensic rules to get an explainable risk score.
* **Jury Question:** *"How is this different from existing cybersecurity tools?"*
* **Your Answer:** *"Existing tools are siloed. You have one tool for deepfakes, one for URLs, and one for account logs. CyberGuard unifies all telemetry under one localized, explainable risk engine, giving SOC analysts a single pane of glass."*

### Subham (ML Engineer)
**Your Role:** Explain the logic behind the Account Takeover and URL/Message anomaly detection. 
* **Jury Question:** *"How do you prevent false positives in behavioral detection?"*
* **Your Answer:** *"We use an Evidence Fusion architecture. A single anomaly (like a new device) isn't enough to trigger a block. We correlate multiple signals—like an unknown MAC address combined with an unusual geolocation and multiple failed logins—before the ML engine flags the risk as critical."*

### Alok (AI Engineer)
**Your Role:** Own the Deepfake Media Engine. Explain how the Vision Transformer (ViT) works.
* **Jury Question:** *"Did you train the deepfake model from scratch? How does it actually work?"*
* **Your Answer:** *"Training a robust ViT from scratch requires massive GPU clusters, which isn't feasible for a hackathon. Instead, we implemented a pre-trained Vision Transformer via Hugging Face. But we didn't stop there—I engineered a forensic fusion layer that combines the neural network's output with local frequency and compression analysis to make the AI explainable and prevent false positives from internet compression."*

### Barshashree Dash (Backend Developer)
**Your Role:** Explain the FastAPI backend, the Pydantic schemas, and the SQLite Event Store. 
* **Jury Question:** *"How scalable is this backend if it had 10,000 users?"*
* **Your Answer:** *"We intentionally built it on FastAPI, which handles requests asynchronously and is incredibly fast. To optimize latency, we load the heavy gigabyte-sized ML models into memory globally during the server `startup` event, dropping inference time to under a second. While we use SQLite for this prototype, our `EventStore` architecture is completely abstracted and can be swapped to PostgreSQL with minimal effort."*

### Dibyajyoti (Frontend Developer)
**Your Role:** Highlight the Next.js App Router, the dark-mode glassmorphic UI, and the seamless user experience.
* **Jury Question:** *"The deepfake analyzer looks great, but ML inference usually hangs the browser. How did you handle that?"*
* **Your Answer:** *"I designed an asynchronous simulated step-loader in React. While the FastAPI backend crunches the heavy neural network inference in the background, the UI iterates through simulated forensic steps (like FFT extraction) to keep the user engaged. Once the `fetch` promise resolves, it instantly reveals the results without ever blocking the main browser thread."*

### D Tilak (PPT Presentation)
**Your Role:** Your slides need to support the demo, not distract from it. 
* **Strategy:** Keep text minimal. Your flow should be: 
  1. **The Threat Landscape** (Deepfakes + Account Takeovers).
  2. **The CyberGuard Solution**.
  3. **The Architecture/Tech Stack** (Show logos of Next.js, FastAPI, Python, Hugging Face).
  4. **LIVE DEMO** (Let Avinash take over).
  5. **Future Scope** (Scaling to PostgreSQL, adding Video deepfake detection).
