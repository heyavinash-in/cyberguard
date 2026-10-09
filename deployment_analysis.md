# Deployment Analysis: Hugging Face Transformers vs. Free Hosting

You asked what would happen if you deployed the PyTorch Hugging Face model (`kmack/malicious-url-detection`) on a free hosting provider like Render, Heroku, or a Serverless platform.

Here is the brutal truth of what will happen: **It will crash immediately.**

## 1. How Much RAM Does It Actually Consume?

When you run `pipeline("text-classification", model="kmack/malicious-url-detection")`, here is roughly how your RAM is eaten up on the server:

| Component | Estimated RAM Usage |
| :--- | :--- |
| **FastAPI / Uvicorn Server Base** | ~50 - 100 MB |
| **PyTorch Core Library** | ~150 - 200 MB |
| **Transformer Model Weights** | ~350 - 500 MB (depending on architecture) |
| **Inference Overhead (Processing the URL)** | ~50 - 100 MB |
| **TOTAL ESTIMATED RAM** | **~650 MB - 900 MB** |

## 2. What Happens on Free Tiers (Render, Vercel, etc.)?

Most free hosting platforms are extremely strict about resources to prevent abuse.

### Render / Heroku / Railway (Free Tiers)
* **The Limit:** Render's free tier gives you a strict maximum of **512 MB of RAM**.
* **What Happens:** When FastAPI starts up and runs `AutoModelForSequenceClassification.from_pretrained()`, the server RAM will spike past 512 MB. 
* **The Result:** The host operating system will trigger an **OOM (Out of Memory) Kill**. Your server logs will just say `Process killed` or `Error 137`, and the server will crash and restart in an endless loop. Your app will never come online.

### Vercel / Netlify (Serverless)
* **The Limit:** Vercel limits Serverless Functions to a maximum unzipped size of **250 MB**.
* **What Happens:** The PyTorch library alone is 120MB+, and the model weights are 300MB+. 
* **The Result:** The build will fail completely. Even if it didn't, spinning up a massive ML model for every single API request ("Cold Start") takes 5-10 seconds, which would cause horrible latency for your users.

## 3. The Solution / Alternatives

If you want to deploy this project for **free**, you have three options:

### Option A: Stick to the Random Forest Model (Recommended for Free Tiers)
The Random Forest model we built using `scikit-learn` is incredibly lightweight. The entire FastAPI server + Scikit-Learn model uses roughly **150 MB of RAM**. It will run flawlessly on a Render Free Tier forever without crashing.

### Option B: Use the Hugging Face Inference API
Instead of hosting the heavy model yourself, you can use the free Hugging Face Inference API. Your backend just sends a lightweight HTTP request to Hugging Face's servers, they do the heavy lifting, and send you the result.
* **Pros:** Costs 0 RAM on your server.
* **Cons:** The free API has rate limits. If your app gets popular, it will be throttled.

### Option C: Upgrade to a Paid Server
If you absolutely want to host the Deep Learning model yourself, you cannot use a free tier. You would need to pay for a standard Docker instance on Render or DigitalOcean (typically the **$7/month to $15/month** tiers which give you 1GB to 2GB of RAM).
