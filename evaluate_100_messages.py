import json
import requests
import time

MESSAGES = [
    # 1-20
    ("Hey, are you free for dinner tonight?", ["SAFE", "LOW"]),
    ("Can you send money to mom when you get home?", ["SAFE", "LOW", "MEDIUM"]),
    ("I transferred the rent to your bank account.", ["SAFE", "LOW"]),
    ("Please remind me to pay the electricity bill tomorrow.", ["SAFE", "LOW"]),
    ("My credit card was charged $999 for the laptop I bought.", ["SAFE", "LOW"]),
    ("Your package should arrive tomorrow afternoon.", ["SAFE", "LOW"]),
    ("I got a notification from Google about my new login.", ["SAFE", "LOW"]),
    ("Google sent me a verification code for my account.", ["SAFE", "LOW"]),
    ("I forgot my password, so I used the official password reset page.", ["SAFE", "LOW"]),
    ("GitHub sent me an email about a new login.", ["SAFE", "LOW"]),
    ("Microsoft asked me to verify my identity after I signed in.", ["SAFE", "LOW"]),
    ("Your OTP is 483921. Use it to complete your login.", ["SAFE", "LOW"]),
    ("I received a bank transaction alert for ₹2,500.", ["SAFE", "LOW"]),
    ("I need to update my address with the bank next week.", ["SAFE", "LOW"]),
    ("Mom asked me to send ₹500 for groceries.", ["SAFE", "LOW", "MEDIUM"]),
    ("Can you check whether my Amazon order has shipped?", ["SAFE", "LOW"]),
    ("I received a delivery notification from the courier.", ["SAFE", "LOW"]),
    ("I got a password-reset email that I requested earlier.", ["SAFE", "LOW"]),
    ("My university sent me a notice about tomorrow's exam.", ["SAFE", "LOW"]),
    ("Please send me the notes when you get a chance.", ["SAFE", "LOW"]),

    # 21-40
    ("Your account will be suspended unless you verify your identity immediately.", ["HIGH", "CRITICAL"]),
    ("Your bank account requires urgent verification. Click the link now.", ["HIGH", "CRITICAL"]),
    ("We detected unusual activity. Confirm your password within 10 minutes.", ["HIGH", "CRITICAL"]),
    ("Your payment failed. Verify your card details immediately.", ["HIGH", "CRITICAL"]),
    ("Your account has been locked. Send your OTP to unlock it.", ["HIGH", "CRITICAL"]),
    ("Security alert: reply with your password to prevent account suspension.", ["HIGH", "CRITICAL"]),
    ("Your refund is waiting. Pay a small processing fee to receive it.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("You have won ₹50,000. Send your bank details to claim your prize.", ["HIGH", "CRITICAL"]),
    ("Your delivery is on hold. Pay ₹99 immediately to release your package.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Your KYC verification has expired. Submit your Aadhaar and bank details now.", ["HIGH", "CRITICAL"]),
    ("This is the bank security team. Tell us the OTP you just received.", ["HIGH", "CRITICAL"]),
    ("We are from customer support. Send your password so we can fix your account.", ["HIGH", "CRITICAL"]),
    ("Your Microsoft account will be deleted today unless you verify it.", ["HIGH", "CRITICAL"]),
    ("Your Google account has been compromised. Confirm your credentials immediately.", ["HIGH", "CRITICAL"]),
    ("Your Netflix subscription has expired. Verify your payment information now.", ["HIGH", "CRITICAL"]),
    ("Your PayPal account is restricted. Confirm your card details to restore access.", ["HIGH", "CRITICAL"]),
    ("Your account has suspicious activity. Click the link and sign in immediately.", ["HIGH", "CRITICAL"]),
    ("You must verify your identity within 5 minutes or your account will be permanently closed.", ["HIGH", "CRITICAL"]),
    ("Failure to respond will result in immediate account suspension.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Do not tell anyone about this verification request. Send the OTP now.", ["HIGH", "CRITICAL"]),

    # 41-55
    ("Send ₹5,000 to this account immediately or your order will be cancelled.", ["HIGH", "CRITICAL"]),
    ("Your bank account is under investigation. Transfer your money to this safe account.", ["HIGH", "CRITICAL"]),
    ("Pay ₹299 to release your government refund.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("We accidentally transferred ₹20,000 to you. Send it back to this UPI ID.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Your electricity bill is overdue. Pay immediately using this link.", ["HIGH", "CRITICAL"]),
    ("Your credit card will be blocked unless you verify your payment details.", ["HIGH", "CRITICAL"]),
    ("Congratulations, you received a ₹10,000 cashback. Pay ₹199 to activate it.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Your investment account has earned ₹80,000. Pay the withdrawal fee to receive it.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Send your UPI PIN to confirm the refund.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Give me your card number and CVV so I can process your refund.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("The bank needs your OTP to reverse the transaction.", ["HIGH", "CRITICAL"]),
    ("Your account balance is at risk. Transfer your funds to the secure account below.", ["HIGH", "CRITICAL"]),
    ("Pay this small verification fee and your loan will be approved today.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Your insurance claim is approved. Send your bank details to receive the payment.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("I need ₹500 from you for mom's medicine.", ["SAFE", "LOW", "MEDIUM"]),

    # 56-70
    ("Send me your password so I can check your account.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Please share the OTP you just received.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("What is your login password?", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Give me the verification code from your phone.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Send your recovery code immediately.", ["HIGH", "CRITICAL"]),
    ("Reply with your username and password to continue.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Your password expires today. Click here to create a new one.", ["HIGH", "CRITICAL"]),
    ("Verify your account by entering your email and password.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Enter your bank login credentials to complete verification.", ["HIGH", "CRITICAL"]),
    ("Send your authentication code to customer support.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Tell me the six-digit code you received.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Your account is at risk. Confirm your password now.", ["HIGH", "CRITICAL"]),
    ("Your session expired. Log in again using the link below.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Please verify your identity by entering your username, password and OTP.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Send your recovery phrase so we can restore your account.", ["MEDIUM", "HIGH", "CRITICAL"]),

    # 71-80
    ("This is the bank security department. Your account has suspicious activity.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("We are calling from Microsoft support regarding your computer.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("This is Google security. Confirm your account credentials.", ["HIGH", "CRITICAL"]),
    ("Government cyber security department: verify your identity immediately.", ["HIGH", "CRITICAL"]),
    ("Police cyber cell notice: pay the required amount to avoid legal action.", ["HIGH", "CRITICAL"]),
    ("Your bank manager has requested your OTP for verification.", ["HIGH", "CRITICAL"]),
    ("Amazon support needs your card details to process your refund.", ["HIGH", "CRITICAL"]),
    ("Microsoft support requires your password to remove the security issue.", ["HIGH", "CRITICAL"]),
    ("Your delivery company requires your Aadhaar number to release the package.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("This is the tax department. Pay the outstanding amount immediately.", ["HIGH", "CRITICAL"]),

    # 81-90
    ("Your A-ccount will be S-uspended unless you v3rify now.", ["HIGH", "CRITICAL"]),
    ("S e n d m e y o u r p a s s w o r d.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Please pass!word check required immediately.", ["HIGH", "CRITICAL"]),
    ("Send y0ur 0TP n0w t0 ver1fy.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Y0ur b@nk acc0unt is l0cked. Cl1ck here n0w.", ["HIGH", "CRITICAL"]),
    ("V3rify y-o-u-r identity or your account will close.", ["HIGH", "CRITICAL"]),
    ("Send the OTP!!! NOW!!! Your account is at risk.", ["HIGH", "CRITICAL"]),
    ("P@ssw0rd and OTP required for account verification.", ["MEDIUM", "HIGH", "CRITICAL"]),
    ("Urgent!!! C0nfirm your c-r-e-d-e-n-t-i-a-l-s immediately.", ["HIGH", "CRITICAL"]),
    ("Your acc0unt will be bl0cked. S e n d O T P n o w.", ["HIGH", "CRITICAL"]),

    # 91-100
    ("Your account is suspended. Verify immediately: https://example.com/login", ["HIGH", "CRITICAL"]),
    ("Bank security alert: confirm your credentials here: https://example.com/verify", ["HIGH", "CRITICAL"]),
    ("Your package is waiting. Pay ₹99 here: https://example.com/delivery", ["HIGH", "CRITICAL"]),
    ("Congratulations! Claim your prize here: https://example.com/reward", ["HIGH", "CRITICAL"]),
    ("Microsoft support: verify your account here: https://example.com/microsoft-login", ["HIGH", "CRITICAL"]),
    ("Check this GitHub repository: https://github.com", ["SAFE", "LOW"]),
    ("I found this interesting article: https://www.wikipedia.org", ["SAFE", "LOW"]),
    ("Your Google account needs verification: https://example.com/google-login", ["HIGH", "CRITICAL"]),
    ("Your refund is ready. Enter your card details here: https://example.com/refund", ["HIGH", "CRITICAL"]),
    ("Security alert!!! Your account will be permanently locked. Send your OTP and verify here: https://example.com/security", ["HIGH", "CRITICAL"])
]

def run_suite():
    print("# CYBERGUARD V1.2 - FINAL 100-MESSAGE REGRESSION SUITE\n")
    print("| ID | MESSAGE | PREDICTED CLASS | RISK SCORE | SEVERITY | CONFIDENCE | EXPECTED SEVERITY | PASS/FAIL | FINDINGS | EVIDENCE GROUPS | ML PROBABILITY | URL RISK CONTRIBUTION |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    
    passed = 0
    failed = 0
    
    for i, (msg, expected_sev) in enumerate(MESSAGES, start=1):
        res = requests.post("http://127.0.0.1:8000/api/analyze/message", json={"message": msg})
        if res.status_code == 200:
            data = res.json()
            sev = data.get("severity", "ERROR")
            risk = data.get("risk_score", 0)
            pred_class = data.get("classification", "UNKNOWN")
            conf = data.get("confidence", 0.0)
            ml_prob = data.get("ml", {}).get("probability", 0.0)
            
            findings = data.get("findings", [])
            finding_cats = [f["category"] for f in findings]
            evidence_groups = []
            url_risk = 0
            
            for f in findings:
                if "URL" in f["category"] or f.get("source") == "url":
                    pass # We will count it below if there is a detailed url finding list, but currently message_risk_engine just adds URL points directly
                for ev in f.get("evidence", []):
                    evidence_groups.append(str(ev))
                    
            # Check if URL engine was triggered
            url_count = data.get("message_features", {}).get("url_count", 0)
            
            # Did it pass?
            is_pass = sev in expected_sev
            
            if is_pass:
                passed += 1
                pf = "✅ PASS"
            else:
                failed += 1
                pf = "❌ FAIL"
                
            print(f"| {i} | `{msg}` | {pred_class} | {risk} | {sev} | {conf} | {' or '.join(expected_sev)} | {pf} | {', '.join(finding_cats)} | {', '.join(evidence_groups)[:50]}... | {ml_prob:.4f} | URLs:{url_count} |")
        else:
            print(f"| {i} | ERROR | | | | | | | | | | |")
            
    print(f"\n**Total:** {len(MESSAGES)} | **Passed:** {passed} | **Failed:** {failed}")

if __name__ == "__main__":
    run_suite()
