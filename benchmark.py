import time
import requests
import numpy as np

URLS_TO_TEST = [
    "https://google.com",
    "https://paypal-security-check.example.com",
    "http://192.168.1.10/login",
    "https://paypa1.com",
    "http://example.com/update.exe",
    "https://netflix.com",
    "https://amazon-verification.example.net/auth"
]

def benchmark():
    times = []
    
    # Warmup
    requests.post("http://127.0.0.1:8000/api/predict", json={"url": "https://example.com"})
    
    for url in URLS_TO_TEST:
        start = time.time()
        res = requests.post("http://127.0.0.1:8000/api/predict", json={"url": url})
        elapsed = time.time() - start
        times.append(elapsed)
        
        data = res.json()
        print(f"URL: {url}")
        print(f"Risk: {data['risk']['score']} | Severity: {data['risk']['severity']}")
        print("-" * 40)
        
    times_ms = [t * 1000 for t in times]
    print("\n=== BENCHMARK RESULTS ===")
    print(f"Average latency: {np.mean(times_ms):.2f} ms")
    print(f"p50 latency: {np.percentile(times_ms, 50):.2f} ms")
    print(f"p95 latency: {np.percentile(times_ms, 95):.2f} ms")

if __name__ == "__main__":
    benchmark()
