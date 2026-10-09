import json
import requests
import time

def evaluate_bias():
    with open('benign_security_validation.json', 'r') as f:
        benign = json.load(f)
    with open('malicious_security_validation.json', 'r') as f:
        malicious = json.load(f)
        
    print("=== BENIGN SET ML BIAS ===")
    total_ml = 0
    total_risk = 0
    fp = 0
    for m in benign:
        res = requests.post("http://127.0.0.1:8000/api/analyze/message", json={"message": m})
        if res.status_code == 200:
            data = res.json()
            ml_prob = data["ml"]["probability"]
            risk = data["risk_score"]
            sev = data["severity"]
            total_ml += ml_prob
            total_risk += risk
            if sev in ["HIGH", "CRITICAL", "MEDIUM"]:  # We'll consider MEDIUM a FP for benign notifications for now to be strict
                fp += 1
            print(f"[{sev}] ML:{ml_prob:.2f} Risk:{risk} | {m}")
    
    print(f"\nAvg ML: {total_ml/len(benign):.2f}, Avg Risk: {total_risk/len(benign):.2f}, FP (Medium/High): {fp}/{len(benign)}\n")
    
    print("=== MALICIOUS SET ML BIAS ===")
    total_ml = 0
    total_risk = 0
    fn = 0
    for m in malicious:
        res = requests.post("http://127.0.0.1:8000/api/analyze/message", json={"message": m})
        if res.status_code == 200:
            data = res.json()
            ml_prob = data["ml"]["probability"]
            risk = data["risk_score"]
            sev = data["severity"]
            total_ml += ml_prob
            total_risk += risk
            if sev in ["SAFE", "LOW"]:
                fn += 1
            print(f"[{sev}] ML:{ml_prob:.2f} Risk:{risk} | {m}")
            
    print(f"\nAvg ML: {total_ml/len(malicious):.2f}, Avg Risk: {total_risk/len(malicious):.2f}, FN (Safe/Low): {fn}/{len(malicious)}\n")

if __name__ == "__main__":
    evaluate_bias()
