import requests

MICRO_TESTS = [
    # Financial manipulation
    ("Your bank account is under investigation. Transfer your money to this secure account.", ["HIGH", "CRITICAL"]),
    ("Your account is at risk. Move your funds to this safe account immediately.", ["HIGH", "CRITICAL"]),
    ("Bank security requires you to transfer your money to a secure account.", ["HIGH", "CRITICAL"]),
    ("I need to transfer rent to my roommate.", ["SAFE", "LOW"]),
    ("I transferred money to my mother yesterday.", ["SAFE", "LOW"]),

    # Question handling
    ("Can you tell me where I can find my recovery code?", ["SAFE", "LOW"]),
    ("What is a recovery code?", ["SAFE", "LOW"]),
    ("How do I reset my password?", ["SAFE", "LOW"]),
    ("Tell me your recovery code.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Send me your OTP.", ["MEDIUM", "HIGH", "CRITICAL"]),

    # Obfuscated advice
    ("D0 n0t share y0ur 0TP with any0ne.", ["SAFE", "LOW"]),
    ("N3ver pr0vide y0ur passw0rd t0 strangers.", ["SAFE", "LOW"]),
    ("D0 n0t t3ll anyone y0ur verification c0de.", ["SAFE", "LOW"]),
    ("S3nd y0ur 0TP n0w.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Pr0vide y0ur passw0rd immediately.", ["MEDIUM", "HIGH", "CRITICAL"]),

    # Obfuscated social engineering
    ("Y0ur bank acc0unt is bl0cked. C0nfirm y0ur c0de n0w.", ["HIGH", "CRITICAL"]),
    ("V3rify y0ur passw0rd immediately or y0ur account will be suspended.", ["HIGH", "CRITICAL"]),
    ("S3nd y0ur UPI PIN n0w t0 receive y0ur refund.", ["HIGH", "CRITICAL"])
]

def run_micro():
    print("Running V1.3.2 Targeted Micro-Tests...")
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
