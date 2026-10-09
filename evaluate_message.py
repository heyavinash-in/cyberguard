import requests
import json
import time

TEST_CASES = [
    # 30 Benign
    {"msg": "Hey, are we still on for lunch today?", "expected": "SAFE/LOW"},
    {"msg": "Google sent me a verification code.", "expected": "SAFE/LOW"},
    {"msg": "I need to reset my password.", "expected": "SAFE/LOW"},
    {"msg": "Amazon delivered my package today.", "expected": "SAFE/LOW"},
    {"msg": "My bank statement is available.", "expected": "SAFE/LOW"},
    {"msg": "I paid my electricity bill.", "expected": "SAFE/LOW"},
    {"msg": "Microsoft released a security update.", "expected": "SAFE/LOW"},
    {"msg": "Please remind me about today's meeting.", "expected": "SAFE/LOW"},
    {"msg": "Can you send money to mom?", "expected": "SAFE/LOW"},
    {"msg": "Check out this cute cat video: https://youtube.com/watch?v=123", "expected": "SAFE/LOW"},
    {"msg": "The weather is nice today.", "expected": "SAFE/LOW"},
    {"msg": "I got a new job!", "expected": "SAFE/LOW"},
    {"msg": "See you at 5 PM.", "expected": "SAFE/LOW"},
    {"msg": "What's the OTP for the Netflix account?", "expected": "SAFE/LOW"},
    {"msg": "I transferred the rent to your bank account.", "expected": "SAFE/LOW"},
    {"msg": "Happy birthday! Hope you have a great day.", "expected": "SAFE/LOW"},
    {"msg": "Did you buy the groceries?", "expected": "SAFE/LOW"},
    {"msg": "Let's go to the movies tonight.", "expected": "SAFE/LOW"},
    {"msg": "Your invoice for last month is attached.", "expected": "SAFE/LOW"},
    {"msg": "Thanks for the help yesterday.", "expected": "SAFE/LOW"},
    {"msg": "I'll call you later.", "expected": "SAFE/LOW"},
    {"msg": "The project deadline is tomorrow.", "expected": "SAFE/LOW"},
    {"msg": "Can you review my code?", "expected": "SAFE/LOW"},
    {"msg": "I'm running 5 minutes late.", "expected": "SAFE/LOW"},
    {"msg": "Did you see the news today?", "expected": "SAFE/LOW"},
    {"msg": "Your Amazon order has shipped.", "expected": "SAFE/LOW"},
    {"msg": "Your payment was successful.", "expected": "SAFE/LOW"},
    {"msg": "Your password reset request was received.", "expected": "SAFE/LOW"},
    {"msg": "Your OTP is 123456.", "expected": "SAFE/LOW"},
    {"msg": "Your account was successfully verified.", "expected": "SAFE/LOW"},

    # 30 Phishing / Social Engineering
    {"msg": "Google Security: send us your verification code immediately or your account will be suspended.", "expected": "HIGH/CRITICAL"},
    {"msg": "Customer support: please send us the OTP you just received to verify your identity.", "expected": "HIGH/CRITICAL"},
    {"msg": "Your bank account has been restricted. Confirm your details immediately using the link below. http://verify-bank.com", "expected": "HIGH/CRITICAL"},
    {"msg": "Tax department notice: your refund is pending. Verify your information now.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Your parcel could not be delivered. Pay the small redelivery fee using this link.", "expected": "HIGH/CRITICAL"},
    {"msg": "Congratulations! Claim your reward by paying the verification fee.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Guaranteed returns available today. Deposit funds now to activate your account.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Microsoft Security: unusual activity detected. Confirm your account immediately.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "URGENT: Your PayPal account is limited. Please update your billing information immediately.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Apple ID: Your account has been locked for security reasons. Click here to unlock: http://apple-support.com", "expected": "HIGH/CRITICAL"},
    {"msg": "Netflix: Your payment was declined. Update your payment method immediately to avoid service termination.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Amazon: You have won a free iPhone! Click the link to claim your prize.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "WhatsApp: Your account will be deactivated in 24 hours. Verify your phone number here.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Facebook: Someone tried to log into your account. Reset your password immediately.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Instagram: Your account has violated our terms of service and will be deleted. Appeal here.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Google: A new login was detected from Russia. If this wasn't you, secure your account now.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "You have a pending package from DHL. Click here to track your shipment and pay customs fees.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Your IRS tax refund of $1,500 is ready. Verify your identity to receive the funds.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "You've been selected for a high-paying remote job. Send us your resume and bank details to start.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Are you lonely? Click here to meet hot singles in your area!", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Invest $100 today and earn $5000 in a week! Join our exclusive crypto trading platform.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Warning: Your computer is infected with a virus. Call Microsoft Technical Support immediately at 1-800-123-4567.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Your subscription to McAfee Antivirus has expired. Renew now to stay protected.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "We have recorded you through your webcam. Pay $1000 in Bitcoin or we will release the video.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Your credit card has been charged $999. If you did not authorize this, click here to cancel.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Confirm your identity by replying with your Social Security Number and Date of Birth.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "You are eligible for a government grant. Pay a small processing fee to receive your money.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Your bank account will be blocked. Enter your OTP at the link below.", "expected": "HIGH/CRITICAL"},
    {"msg": "Your email inbox is almost full. Upgrade your storage now or you will stop receiving emails.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Please review this important document attached to this email.", "expected": "MEDIUM/HIGH/CRITICAL"},

    # Borderline
    {"msg": "Please verify your account.", "expected": "MEDIUM/LOW"},
    {"msg": "Your payment was declined.", "expected": "MEDIUM/LOW"},
    {"msg": "Security update available.", "expected": "MEDIUM/LOW"},
    {"msg": "Click here to view your invoice.", "expected": "MEDIUM/LOW"},
    {"msg": "Action required on your account.", "expected": "MEDIUM/LOW"},
    {"msg": "Login attempt from a new device.", "expected": "MEDIUM/LOW"},
    {"msg": "Your subscription is renewing soon.", "expected": "MEDIUM/LOW"},
    {"msg": "Review your recent transactions.", "expected": "MEDIUM/LOW"},
    {"msg": "Important notice regarding your policy.", "expected": "MEDIUM/LOW"},
    {"msg": "Dear Customer, \n\n\n\n\nPlease pay your bill.", "expected": "MEDIUM/LOW"},

    # URL-Heavy
    {"msg": "Please review this account notice: https://suspicious-domain.example/login", "expected": "HIGH/CRITICAL"},
    {"msg": "Here is the documentation: https://github.com/login", "expected": "SAFE/LOW"},
    {"msg": "Check these links: https://example.com, https://google.com, https://microsoft.com", "expected": "SAFE/LOW"},
    {"msg": "Verify here: http://192.168.1.1/login", "expected": "HIGH/CRITICAL"},
    {"msg": "Download the file: https://example.com/malware.exe", "expected": "HIGH/CRITICAL"},
    {"msg": "Read this article: https://en.wikipedia.org/wiki/Phishing", "expected": "SAFE/LOW"},
    {"msg": "Update your payment: https://netflix-billing.example.net/payment/update", "expected": "HIGH/CRITICAL"},
    {"msg": "My portfolio: https://my-website.com", "expected": "SAFE/LOW"},
    {"msg": "Claim prize: https://free-money-now.xyz", "expected": "HIGH/CRITICAL"},
    {"msg": "Watch this: https://youtube.com/watch?v=dQw4w9WgXcQ", "expected": "SAFE/LOW"},

    # Adversarial (Normalization targets)
    {"msg": "Your A-ccount will be S-uspended. Verify your password immediately.", "expected": "HIGH/CRITICAL"},
    {"msg": "S e n d m e y o u r p a s s w o r d to complete verification.", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "v3r1fy y0ur b4nk acc0unt", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "p4ssword", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "0tp required now", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Enter your p.a.s.s.w.o.r.d here", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Please pass!word check", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "Click here: https://example.com?redirect=http://evil.com", "expected": "HIGH/CRITICAL"},
    {"msg": "Verify identity immediately immediately immediately immediately immediately immediately immediately", "expected": "MEDIUM/HIGH/CRITICAL"},
    {"msg": "A" * 5000, "expected": "SAFE/LOW/ERROR"} 
]

def run_tests():
    total = len(TEST_CASES)
    passed = 0
    failed = 0
    fp = 0
    fn = 0
    
    start_time = time.time()
    
    print("| # | Expected | Actual | Risk | Message Snippet | Pass/Fail |")
    print("| - | -------- | ------ | ---- | --------------- | --------- |")
    
    for i, tc in enumerate(TEST_CASES):
        msg = tc["msg"]
        expected = tc["expected"]
        
        try:
            res = requests.post("http://127.0.0.1:8000/api/analyze/message", json={"message": msg}, timeout=5)
            if res.status_code == 200:
                data = res.json()
                actual = data["severity"]
                risk = data["risk_score"]
            else:
                actual = "ERROR"
                risk = 0
        except Exception as e:
            actual = "ERROR"
            risk = 0
            
        expected_options = expected.split('/')
        pass_fail = "Pass" if actual in expected_options else "Fail"
        
        if pass_fail == "Fail":
            is_expected_safe = "SAFE" in expected_options or "LOW" in expected_options or "MEDIUM" in expected_options
            is_actual_safe = actual in ["SAFE", "LOW", "MEDIUM"]
            
            if is_expected_safe and not is_actual_safe:
                fp += 1
            elif not is_expected_safe and is_actual_safe:
                fn += 1
                
        if pass_fail == "Pass":
            passed += 1
        else:
            failed += 1
            
        snippet = msg[:40].replace('\n', ' ') + "..." if len(msg) > 40 else msg.replace('\n', ' ')
        print(f"| {i+1} | {expected} | {actual} | {risk} | `{snippet}` | {pass_fail} |")
        
    end_time = time.time()
    latency = (end_time - start_time) / total * 1000
    
    print("\n### Evaluation Metrics\n")
    print(f"**Total tests:** {total}")
    print(f"**Passed:** {passed}")
    print(f"**Failed:** {failed}")
    print(f"**False Positives:** {fp}")
    print(f"**False Negatives:** {fn}")
    print(f"**Average Latency:** {latency:.2f} ms")

if __name__ == "__main__":
    run_tests()
