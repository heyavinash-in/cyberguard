import re
from typing import List, Dict, Any, Tuple
from .message_normalizer import normalize_message

REQUEST_VERBS = r'(send|share|enter|reply|verify|provide|confirm|update|tell|submit|type|give|message|forward|need|require|ask|request|reveal|disclose|return|upload)'

SOCIAL_ENGINEERING_PATTERNS = {
    "INFORMATIONAL_QUESTION": [
        r'where (i can|can i|do i|to) find.{0,25}(recovery_code|otp|password|passcode|credential|code)',
        r'what is (a |your |my )?(recovery_code|otp|password|passcode|code)',
        r'how do i (reset|find|get).{0,25}(recovery_code|otp|password|passcode|credential|code)',
        r'where do i (enter|put|type).{0,25}(recovery_code|otp|password|passcode|credential|code)'
    ],
    "URGENCY_PRESSURE": [
        r'urgent', r'immediately', r'act now', r'within \d+ (minutes|hours|days)',
        r'expires? today', r'last warning', r'final notice', r'respond immediately',
        r'action required', r'now or', r'without delay', r'at risk'
    ],
    "THREAT_OR_CONSEQUENCE": [
        r'account (is|will be|has been) (suspended|blocked|locked|closed|restricted|under investigation)',
        r'legal action', r'penalty', r'fine', r'service termination',
        r'access (will be|has been) revoked', r'cancel your', r'terminate your',
        r'deactivated', r'permanently closed', r'will close', r'under investigation'
    ],
    "SECURITY_ADVICE": [
        r'(never|do not|don\'t).{0,15}(share|send|give|tell|provide|reveal|enter|submit).{0,35}(otp|password|code|pin|credential|information|detail)',
        r'(no one|staff|bank|support).{0,15}(will|should) (ever|never) ask',
        r'remember not to share'
    ],
    "CREDENTIAL_MENTION": [
        r'password', r'username', r'login', r'sign in', r'credentials', 
        r'recovery phrase', r'recovery_code', r'passcode', r'pass phrase', r'seed phrase', r'backup code'
    ],
    "CREDENTIAL_REQUEST": [
        REQUEST_VERBS + r'.{0,35}(password|username|login|credentials|account|recovery phrase|recovery_code|passcode|pass phrase|seed phrase|authentication_code|pin|backup code)',
        r'(password|username|login|credentials|account|recovery phrase|recovery_code|passcode|pass phrase|seed phrase|authentication_code|pin|backup code).{0,25}(is required|needed|requested)',
        r'verify (your )?(identity|account)', r'security verification',
        r'update your account', r'pass!word check', r'confirm your credentials'
    ],
    "OTP_MENTION": [
        r'otp', r'verification_code', r'security_code',
        r'six digit code', r'authentication_code', r'six-digit code', r'6 digit code', r'auth_code', r'\bcode\b'
    ],
    "OTP_REQUEST": [
        REQUEST_VERBS + r'.{0,35}(otp|verification_code|security_code|six digit code|six-digit code|authentication_code|auth_code|\bcode\b)',
        r'(otp|verification_code|security_code|six digit code|six-digit code|authentication_code|auth_code|\bcode\b).{0,25}(is required|needed|requested)'
    ],
    "CARD_DETAILS_REQUEST": [
        REQUEST_VERBS + r'.{0,35}(card number|cvv|cvc|upi pin|bank credentials|card details|bank details|aadhaar|pan|government id|identity document|payment information|payment details|billing information|billing details|payment method|financial information|account credentials)',
        r'(card number|cvv|cvc|upi pin|bank credentials|card details|bank details|aadhaar|pan|government id|identity document|payment information|payment details|billing information|billing details|payment method|financial information|account credentials).{0,25}(is required|needed|requested)'
    ],
    "FINANCIAL_TRANSFER_MANIPULATION": [
        r'(transfer|move|send) (your|the)? (money|funds|balance)',
        r'(transfer|move|send|deposit) (it |them )?(to|into) this (secure|safe|new)? ?account',
        r'send funds for verification'
    ],
    "FINANCIAL_MENTION": [
        r'bank account', r'refund', r'invoice', r'wallet', r'crypto', r'billing',
        r'payment', r'transaction', r'statement', r'loan'
    ],
    "FINANCIAL_REQUEST": [
        r'send money', r'transfer money', r'pay now', r'payment required', r'pay.{0,25}fee',
        r'deposit funds', r'pay.{0,15}bill', r'pay the required amount', r'pay the outstanding amount'
    ],
    "REWARD_LURE": [
        r'you (have )?won', r'congratulations', r'lottery', r'prize',
        r'reward', r'cashback', r'free gift', r'claim your', r'limited offer',
        r'guaranteed returns', r'free (iphone|money)'
    ],
    "AUTHORITY_MENTION": [
        r'bank', r'government', r'police', r'tax department', r'income tax',
        r'court', r'microsoft', r'google', r'amazon', r'paypal', r'instagram',
        r'facebook', r'netflix', r'apple', r'dhl', r'irs', r'cyber cell', r'delivery company'
    ],
    "AUTHORITY_CLAIM": [
        r'(microsoft|google|amazon|paypal|instagram|facebook|netflix|apple|bank|tax department|police|government|dhl) (security|support|technical|team|manager|cyber cell|notice)',
        r'technical support', r'customer support', r'security team', r'tax department notice', r'irs notice',
        r'(this is|we are|calling from|message from).{0,25}(bank|microsoft|google|amazon|paypal|police|government|tax|support|security|delivery)',
        r'(bank|microsoft|google|amazon|paypal|police|government|tax|support|security|delivery).{0,25}(requires|requests|needs|asked)'
    ]
}

def extract_urls(text: str) -> List[str]:
    url_pattern = r'(?:https?://|www\.)[^\s]+'
    raw_urls = re.findall(url_pattern, text)
    clean_urls = []
    for url in raw_urls:
        url = url.rstrip('.,!?:;')
        if url.startswith('www.'):
            url = 'http://' + url
        clean_urls.append(url)
    return clean_urls

def preprocess_text(text: str) -> str:
    norm_text, _ = normalize_message(text)
    norm_text = re.sub(r'(?:https?://|www\.)[^\s]+', 'URL_TOKEN', norm_text)
    norm_text = re.sub(r'\S+@\S+', 'EMAIL_TOKEN', norm_text)
    norm_text = re.sub(r'\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', 'PHONE_TOKEN', norm_text)
    norm_text = re.sub(r'\b\d+\b', 'DIGIT_TOKEN', norm_text)
    return norm_text

class MessageFeatureExtractor:
    def __init__(self):
        pass
        
    def extract_features(self, message: str, sender: str = None, subject: str = None) -> Tuple[Dict[str, Any], List[str]]:
        features = {}
        
        # 1. Structural features
        features["message_length"] = len(message)
        features["word_count"] = len(message.split())
        features["uppercase_ratio"] = sum(1 for c in message if c.isupper()) / max(1, len(message))
        features["digit_ratio"] = sum(1 for c in message if c.isdigit()) / max(1, len(message))
        features["exclamation_count"] = message.count('!')
        features["question_count"] = message.count('?')
        
        extracted_urls = extract_urls(message)
        features["url_count"] = len(extracted_urls)
        features["has_url"] = features["url_count"] > 0
        
        # 2. Normalization
        norm_msg, norm_findings = normalize_message(message)
        features["normalization_findings"] = norm_findings
        features["has_excessive_spacing"] = "spaced_out_words" in norm_findings
        features["has_leet_speak"] = "leetspeak" in norm_findings
        
        # 3. Social Engineering Pattern Matching
        msg_lower = message.lower()
        search_texts = [msg_lower, norm_msg]
            
        se_matches = {}
        for category, patterns in SOCIAL_ENGINEERING_PATTERNS.items():
            matches = []
            for pattern in patterns:
                for i, st in enumerate(search_texts):
                    found = re.findall(pattern, st)
                    if found:
                        matches.extend([m if isinstance(m, str) else m[0] for m in found])
                        if category in ["SECURITY_ADVICE", "INFORMATIONAL_QUESTION"]:
                            # Mask out the advice/question portion so it doesn't trigger requests
                            search_texts[i] = re.sub(pattern, " [MASK] ", st)
            
            if subject:
                subj_lower = subject.lower()
                for pattern in patterns:
                    found = re.findall(pattern, subj_lower)
                    if found:
                        matches.extend([m if isinstance(m, str) else m[0] for m in found])
                        
            if matches:
                se_matches[category] = list(set(matches))
                
        features["se_matches"] = se_matches
        
        # Security Advice / Negation overrides harvesting slightly
        has_advice = "SECURITY_ADVICE" in se_matches
        features["has_security_advice"] = has_advice
        
        # Resolve Request vs Mention
        has_cred_req = "CREDENTIAL_REQUEST" in se_matches
        has_otp_req = "OTP_REQUEST" in se_matches
        has_card_req = "CARD_DETAILS_REQUEST" in se_matches
        has_fin_req = "FINANCIAL_REQUEST" in se_matches
        
        # If the only "request" is negated by safety advice, don't flag as request
        # (A real model would parse dependency tree, but this is a heuristic fallback)
        if has_advice and not (has_cred_req or has_otp_req or has_card_req):
            pass # Keep logic simple for now
            
        features["has_credential_request"] = has_cred_req
        features["has_otp_request"] = has_otp_req
        features["has_card_request"] = has_card_req
        features["has_payment_request"] = has_fin_req
        features["has_financial_transfer"] = "FINANCIAL_TRANSFER_MANIPULATION" in se_matches
        features["has_informational_question"] = "INFORMATIONAL_QUESTION" in se_matches
        
        # Mentions
        features["has_credential_mention"] = "CREDENTIAL_MENTION" in se_matches and not has_cred_req
        features["has_otp_mention"] = "OTP_MENTION" in se_matches and not has_otp_req
        features["has_payment_mention"] = "FINANCIAL_MENTION" in se_matches and not has_fin_req
        
        features["has_urgency"] = "URGENCY_PRESSURE" in se_matches
        features["has_threat"] = "THREAT_OR_CONSEQUENCE" in se_matches
        features["has_reward"] = "REWARD_LURE" in se_matches
        
        has_auth_claim = "AUTHORITY_CLAIM" in se_matches
        features["has_authority_claim"] = has_auth_claim
        features["has_authority_mention"] = "AUTHORITY_MENTION" in se_matches and not has_auth_claim
        
        features["sender_suspicious"] = False
        if sender and any(domain in sender.lower() for domain in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']):
            if features["has_authority_claim"] or features["has_authority_mention"]:
                features["sender_suspicious"] = True
                    
        return features, extracted_urls
