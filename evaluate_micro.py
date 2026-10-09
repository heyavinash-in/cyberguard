import json
import requests

MICRO_TESTS = [
    # Security advice
    ("Never share your OTP.", ["SAFE", "LOW"]),
    ("Do not tell anyone your verification code.", ["SAFE", "LOW"]),
    ("Bank staff will never ask for your password.", ["SAFE", "LOW"]),
    ("Do not provide your recovery code.", ["SAFE", "LOW"]),
    
    # Actual harvesting
    ("Send me your OTP.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Tell me your verification code.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Provide your password.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Share your recovery code.", ["MEDIUM", "HIGH", "CRITICAL"]),
    
    # Compound normalization
    ("Confirm your pass code.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Confirm your pass-code.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Confirm your pass_code.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Enter your verification code.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Enter your one-time password.", ["MEDIUM", "HIGH", "CRITICAL"]),
    
    # Payment information
    ("Verify your payment information.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Send your payment details.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Never share your payment information.", ["SAFE", "LOW"]),
    ("Your payment information was updated.", ["SAFE", "LOW"]),
    
    # Impersonation
    ("This is the bank security department.", ["LOW", "MEDIUM"]),
    ("This is the bank security department. Send your OTP.", ["HIGH", "CRITICAL"]),
    ("This is Microsoft support. Provide your password.", ["HIGH", "CRITICAL"]),
    ("This is the delivery company. Pay the fee immediately.", ["HIGH", "CRITICAL"]),
    
    # Mixed benign/security
    ("Google sent me a verification code.", ["SAFE", "LOW"]),
    ("I received an OTP from my bank.", ["SAFE", "LOW"]),
    ("Please use the official website to reset your password.", ["SAFE", "LOW"])
]

def run_micro():
    print("Running V1.3.1 Micro-Tests...")
    passed = 0
    
    for i, (msg, expected_sev) in enumerate(MICRO_TESTS, start=1):
        res = requests.post("http://127.0.0.1:8000/api/analyze/message", json={"message": msg})
        if res.status_code == 200:
            data = res.json()
            sev = data.get("severity", "ERROR")
            risk = data.get("risk_score", 0)
            
            is_pass = sev in expected_sev
            if is_pass:
                passed += 1
                pf = "PASS"
            else:
                pf = "FAIL"
                
            print(f"[{pf}] {sev} ({risk}) | Expected: {' or '.join(expected_sev)} | '{msg}'")
        else:
            print(f"[ERROR] '{msg}'")

    print(f"\nMicro-Tests: {passed}/{len(MICRO_TESTS)} passed.")

if __name__ == "__main__":
    run_micro()
