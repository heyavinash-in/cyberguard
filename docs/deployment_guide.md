# CyberGuard Deployment Guide

Since you have two distinct architectures (a Next.js React frontend and a heavy FastAPI Python backend), the best approach for a quick hackathon deployment is to split them across two specialized cloud providers.

This ensures you don't run into memory limits (OOM) due to the 350MB+ Hugging Face Vision Transformer model.

---

## 1. Deploying the Backend (FastAPI + AI Models)

Because your backend uses PyTorch and Hugging Face pipelines, it needs more RAM than standard free tiers provide. **Render.com** (Free tier) or **Hugging Face Spaces** are the best options. We will use Render for standard REST API hosting.

*I have already generated and pushed the required `backend/requirements.txt` to your GitHub repo.*

### Steps for Render.com (Recommended)
1. Go to [Render.com](https://render.com) and sign in with GitHub.
2. Click **New +** and select **Web Service**.
3. Select your repository: `heyavinash-in/cyberguard`.
4. Configure the service:
   * **Name:** `cyberguard-api`
   * **Root Directory:** `backend` (CRITICAL: ensure this is set so Render finds the requirements.txt)
   * **Environment:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Click **Create Web Service**. 
6. *Note: Render's free tier takes about 50 seconds to spin up after sleeping. For a live demo, ping it a minute before you present to wake it up!*

---

## 2. Deploying the Frontend (Next.js Dashboard)

The frontend is built with Next.js, making **Vercel** the absolute best and easiest place to deploy it.

### Steps for Vercel
1. Go to [Vercel.com](https://vercel.com) and log in with GitHub.
2. Click **Add New -> Project**.
3. Import your repository: `heyavinash-in/cyberguard`.
4. Vercel will automatically detect that it is a Next.js project.
5. Expand the **Environment Variables** section. You need to tell the frontend where the cloud backend lives (instead of localhost).
   * **Key:** `NEXT_PUBLIC_API_BASE_URL`
   * **Value:** `https://your-render-backend-url.onrender.com` *(Replace this with the actual URL Render gives you in Step 1).*
6. Click **Deploy**.

---

## 3. Alternative: Localhost for the Pitch (Fallback Plan)

If the cloud deployment fails or the free-tier servers are too slow to load the heavy Deepfake model during the live presentation, **DO NOT PANIC.** 

It is incredibly common (and often preferred) in hackathons to present the live demo locally to avoid internet latency, and simply provide the GitHub link as proof of code.

To run it locally for the jury, just execute the two commands I set up for you:
1. `cmd /c npm run dev`
2. `python -m uvicorn app.main:app --port 8000`
