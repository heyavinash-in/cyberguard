import requests

MESSAGES = [
    "Hey, are we still meeting for lunch today?",
    "Please send me the notes from yesterday's class.",
    "I received a verification code from Google.",
    "Never share your OTP with anyone.",
    "My bank sent me an OTP for my transaction.",
    "Do not tell anyone your verification code.",
    "Can you send the project file when you get time?",
    "I need to transfer rent to my roommate today.",
    "Your payment information was updated successfully.",
    "I forgot my password and need to reset it.",
    "Your account will be suspended unless you verify immediately.",
    "Your bank account has suspicious activity. Verify your account now.",
    "Send me your OTP immediately to prevent your account from being blocked.",
    "Tell me your login password to complete the verification.",
    "Provide your recovery code to restore your account.",
    "Confirm your pass code to complete the request.",
    "Confirm your pass-code to complete the request.",
    "Confirm your pass_code to complete the request.",
    "Enter your verification code to continue.",
    "Enter your one-time password to complete verification.",
    "Never share your password with someone who contacts you unexpectedly.",
    "Bank staff will never ask you for your OTP.",
    "Do not provide your recovery code to anyone.",
    "Please use the official bank website to reset your password.",
    "Your Netflix subscription has expired. Verify your payment information now.",
    "Your payment details are required to process the refund.",
    "Send your payment information to receive the refund.",
    "Never share your payment information over an unsolicited message.",
    "Your card number is required to complete this verification.",
    "Please provide your card number and CVV to confirm the payment.",
    "Enter your UPI PIN to receive the refund.",
    "Send your UPI PIN immediately or the transaction will fail.",
    "Your credit card was charged successfully.",
    "I checked my credit card statement this morning.",
    "My payment information was updated yesterday.",
    "Can you tell me where I can find my recovery code?",
    "What is a recovery code used for?",
    "I received a six-digit verification code from my bank.",
    "Google sent me a verification code for my login.",
    "I received an OTP after signing into my account.",
    "This is the bank security department. Your account has suspicious activity.",
    "This is the bank security department. Send your OTP immediately.",
    "This is Microsoft support. Your account has been compromised.",
    "This is Microsoft support. Provide your password to secure your account.",
    "Google Security has detected unusual activity. Verify your credentials now.",
    "This is Amazon customer support. Confirm your card details immediately.",
    "Your delivery company needs your Aadhaar number to release the package.",
    "This is the tax department. Pay the pending amount immediately.",
    "The police cyber cell requires your payment details for investigation.",
    "This is customer support. Tell us your authentication code.",
    "Your account will be locked in 10 minutes unless you verify your password.",
    "Your account is at risk. Send your OTP now.",
    "Your password expires today. Click the link to keep your account active.",
    "Your recovery code is required immediately to prevent account suspension.",
    "Please confirm your credentials to continue using your account.",
    "Send your username and password to verify ownership.",
    "Enter your email and password on the verification page.",
    "Provide your bank credentials immediately.",
    "Share your authentication code with customer support.",
    "Send your six-digit code to complete account verification.",
    "Give me your login password so I can verify your account.",
    "Please provide your PAN number for the account verification.",
    "Submit your Aadhaar number to complete KYC verification.",
    "Send your government ID to confirm your identity.",
    "Provide your debit card number and CVV immediately.",
    "Tell me your UPI PIN so I can process the refund.",
    "Send your recovery phrase to restore your wallet.",
    "Provide your backup code to unlock your account.",
    "Your account has been compromised. Confirm your password immediately.",
    "Your security team needs your OTP right now.",
    "URGENT: Your account is blocked. Send your password immediately.",
    "Your bank account will be closed unless you verify your identity now.",
    "You have won a reward. Send your bank details to claim it.",
    "Congratulations! Pay a small processing fee to receive your prize.",
    "Your refund is waiting. Provide your card details to receive it.",
    "You have received a cashback reward. Pay the verification fee now.",
    "Your electricity bill is overdue. Pay immediately using this link.",
    "Your bank account is under investigation. Transfer your money to this secure account.",
    "We accidentally transferred money to you. Send it back to this UPI ID immediately.",
    "Your government refund requires a small payment before release.",
    "Your account is suspended. V3rify your password immediately.",
    "S e n d y o u r O T P n o w.",
    "Your p-a-s-s-w-o-r-d is required for verification.",
    "Your account is l0cked. Pr0vide your 0TP immediately.",
    "V3rify your 1dent1ty or your account will be suspended.",
    "Send y0ur passw0rd and 0TP t0 unlock the account.",
    "Y0ur bank acc0unt is bl0cked. C0nfirm y0ur c0de n0w.",
    "D0 n0t share y0ur 0TP with any0ne.",
    "N3ver pr0vide y0ur passw0rd t0 strangers.",
    "Y0ur acc0unt will be cl0sed unless y0u ver1fy 1mmed1ately.",
    "Your account is suspended. Verify here: http://example.com/login",
    "Bank security alert: send your credentials here: http://example.com/verify",
    "Your package is waiting. Pay the delivery fee here: http://example.com/pay",
    "Congratulations! Claim your prize here: http://example.com/reward",
    "Microsoft support says your account is compromised. Verify here: http://example.com/microsoft",
    "Check the project repository here: https://github.com/example/project",
    "You can read the article here: https://en.wikipedia.org/wiki/Computer_security",
    "Google verification required. Confirm your account here: http://example.com/google-login",
    "Your refund is ready. Send your card details here: http://example.com/refund",
    "SECURITY ALERT: Your account will be locked. Send your OTP immediately: http://example.com/security"
]

def run():
    print("| ID | Message | Risk Score | Severity | Classification |")
    print("|---|---|---|---|---|")
    for i, msg in enumerate(MESSAGES, start=1):
        res = requests.post("http://127.0.0.1:8000/api/analyze/message", json={"message": msg})
        if res.status_code == 200:
            data = res.json()
            risk = data.get("risk_score", 0)
            sev = data.get("severity", "ERROR")
            cls = data.get("classification", "UNKNOWN")
            # Replace newlines with spaces so table doesn't break
            safe_msg = msg.replace("\n", " ")
            print(f"| {i} | `{safe_msg}` | {risk} | {sev} | {cls} |")
        else:
            print(f"| {i} | ERROR | | | |")

if __name__ == "__main__":
    run()
