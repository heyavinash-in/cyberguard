import re
import math
import urllib.parse
try:
    import tldextract
except ImportError:
    tldextract = None

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def normalized_similarity(s1: str, s2: str) -> float:
    if not s1 and not s2: return 1.0
    if not s1 or not s2: return 0.0
    dist = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1.0 - (dist / max_len)

def visual_normalize(s: str) -> str:
    # Normalize common visual substitutions attackers use
    s = s.lower()
    replacements = {
        '0': 'o',
        '1': 'l',
        '3': 'e',
        '4': 'a',
        '5': 's',
        '@': 'a',
        '8': 'b',
        'rn': 'm' # common kerning trick
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s

BRAND_CONFIG = {
    "microsoft": {
        "official_domains": ["microsoft.com", "microsoftonline.com", "live.com", "office.com", "office365.com", "skype.com"],
        "keywords": ["microsoft", "office365", "windows"]
    },
    "apple": {
        "official_domains": ["apple.com", "appleid.com", "icloud.com"],
        "keywords": ["apple", "icloud"]
    },
    "google": {
        "official_domains": ["google.com", "googleusercontent.com", "gmail.com", "youtube.com"],
        "keywords": ["google", "gmail", "youtube"]
    },
    "adobe": {
        "official_domains": ["adobe.com"],
        "keywords": ["adobe"]
    },
    "cloudflare": {
        "official_domains": ["cloudflare.com"],
        "keywords": ["cloudflare"]
    },
    "paypal": {
        "official_domains": ["paypal.com"],
        "keywords": ["paypal"]
    },
    "amazon": {
        "official_domains": ["amazon.com", "amazon.in", "amazon.co.uk", "aws.amazon.com"],
        "keywords": ["amazon", "aws"]
    },
    "netflix": {
        "official_domains": ["netflix.com"],
        "keywords": ["netflix"]
    },
    "github": {
        "official_domains": ["github.com", "githubusercontent.com"],
        "keywords": ["github"]
    },
    "linkedin": {
        "official_domains": ["linkedin.com"],
        "keywords": ["linkedin"]
    },
    "facebook": {
        "official_domains": ["facebook.com", "fb.com"],
        "keywords": ["facebook", "meta"]
    },
    "instagram": {
        "official_domains": ["instagram.com"],
        "keywords": ["instagram"]
    },
    "nasa": {
        "official_domains": ["nasa.gov"],
        "keywords": ["nasa"]
    }
}

SUSPICIOUS_KEYWORDS = {
    "auth": ["login", "signin", "sign-in", "verify", "verification", "authenticate", "account", "password", "credential", "secure", "security"],
    "urgency": ["urgent", "immediately", "suspended", "expire", "expired", "action-required", "warning", "alert"],
    "finance": ["bank", "payment", "invoice", "refund", "wallet", "transaction", "billing", "card"],
    "recovery": ["reset", "recover", "unlock", "confirm", "validate"]
}

SUSPICIOUS_TLDS = {'xyz', 'top', 'cc', 'tk', 'gq', 'cf', 'pw', 'info', 'biz', 'vip', 'club', 'online', 'site', 'ru', 'cn'}

def calculate_entropy(text):
    if not text: return 0
    entropy = 0
    for x in set(text):
        p_x = float(text.count(x)) / len(text)
        entropy += - p_x * math.log2(p_x)
    return entropy

class StaticFeatureExtractor:
    def __init__(self):
        pass

    def extract(self, normalized_data: dict) -> dict:
        url = normalized_data["normalized_url"]
        parsed = normalized_data["parsed"]
        hostname = normalized_data.get("hostname", "")
        path = parsed.path or ""
        query = parsed.query or ""
        
        features = {}
        
        # 1. Basic URL Features
        features["url_length"] = len(url)
        features["hostname_length"] = len(hostname)
        features["path_length"] = len(path)
        features["query_length"] = len(query)
        features["fragment_length"] = len(parsed.fragment or "")
        features["num_path_segments"] = len([p for p in path.split('/') if p])
        features["num_query_params"] = len(urllib.parse.parse_qsl(query))
        features["num_dots"] = url.count('.')
        features["num_hyphens"] = url.count('-')
        features["num_underscores"] = url.count('_')
        features["num_digits"] = sum(c.isdigit() for c in url)
        features["num_special_chars"] = sum(not c.isalnum() for c in url)
        features["num_pct"] = url.count('%')
        
        # 2. Protocol / Security
        features["is_https"] = 1 if parsed.scheme == "https" else 0
        features["is_http"] = 1 if parsed.scheme == "http" else 0
        try:
            features["has_port"] = 1 if parsed.port else 0
        except ValueError:
            features["has_port"] = 1
        
        # 3. IP Address
        is_ipv4 = bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname))
        is_ipv6 = bool(re.match(r'^\[[0-9a-fA-F:]+\]$', hostname))
        features["is_ip_address"] = 1 if is_ipv4 or is_ipv6 else 0
        
        # 4. Domain & Subdomain Analysis
        domain = hostname
        subdomain = ""
        tld = ""
        if tldextract and not features["is_ip_address"]:
            ext = tldextract.extract(hostname)
            domain = ext.domain
            subdomain = ext.subdomain
            tld = ext.suffix
            
        registrable_domain = f"{domain}.{tld}" if tld else domain
        features["registrable_domain"] = registrable_domain
        
        # 5. Brand Impersonation & Typosquatting
        features["brand_in_subdomain"] = 0
        features["brand_impersonation"] = 0
        features["typosquatting"] = 0
        features["legit_brand"] = 0
        features["suspected_brand"] = ""
        features["typo_similarity"] = 0.0
        
        is_official = False
        # First pass: check if it's an official domain
        for brand, conf in BRAND_CONFIG.items():
            if registrable_domain in conf["official_domains"]:
                is_official = True
                features["legit_brand"] = 1
                features["suspected_brand"] = brand
                break
                
        # If not official, check for impersonation
        if not is_official and not features["is_ip_address"]:
            domain_label = domain.lower()
            normalized_domain_label = visual_normalize(domain_label)
            
            for brand, conf in BRAND_CONFIG.items():
                for kw in conf["keywords"]:
                    # Brand in subdomain
                    if kw in subdomain.lower().replace('-', ''):
                        features["brand_in_subdomain"] = 1
                        features["suspected_brand"] = brand
                    
                    # Direct substring impersonation in domain
                    stripped_label = domain_label.replace('-', '')
                    if kw in stripped_label and domain_label != kw:
                        features["brand_impersonation"] = 1
                        features["suspected_brand"] = brand
                        
                    # Direct exact match impersonation (e.g., google.xyz)
                    if domain_label == kw:
                        features["brand_impersonation"] = 1
                        features["suspected_brand"] = brand
                        continue # Handled by brand_impersonation, skip typo
                        
                    # Typosquatting (Levenshtein)
                    # We check against the raw label AND the visually normalized label
                    sim_raw = normalized_similarity(domain_label, kw)
                    sim_norm = normalized_similarity(normalized_domain_label, kw)
                    best_sim = max(sim_raw, sim_norm)
                    
                    # A similarity >= 0.75 for a decent length keyword is suspicious
                    if best_sim >= 0.75 and len(kw) >= 4:
                        features["typosquatting"] = 1
                        if best_sim > features["typo_similarity"]:
                            features["typo_similarity"] = round(best_sim, 2)
                            features["suspected_brand"] = brand

        # 6. Punycode
        features["has_punycode"] = 1 if "xn--" in hostname.lower() else 0
        
        # 7. Keyword Analysis
        url_lower = url.lower()
        features["kw_auth"] = 1 if any(kw in url_lower for kw in SUSPICIOUS_KEYWORDS["auth"]) else 0
        features["kw_urgency"] = 1 if any(kw in url_lower for kw in SUSPICIOUS_KEYWORDS["urgency"]) else 0
        features["kw_finance"] = 1 if any(kw in url_lower for kw in SUSPICIOUS_KEYWORDS["finance"]) else 0
        
        # 8. Path Analysis (suspicious files)
        suspicious_exts = {'.exe', '.scr', '.bat', '.cmd', '.zip', '.apk', '.msi', '.js'}
        features["suspicious_file_ext"] = 1 if any(path.lower().endswith(ext) for ext in suspicious_exts) else 0
        
        # 9. Obfuscation & Nested
        features["nested_url"] = 1 if re.search(r'(url|redirect|redirect_url|next|return|continue|target|dest|destination)=https?%3A%2F%2F', query, re.I) else 0
        features["excessive_encoding"] = 1 if features["num_pct"] > 5 else 0
        
        # 10. Suspicious TLD
        features["suspicious_tld"] = 1 if tld.lower() in SUSPICIOUS_TLDS else 0
        
        # 11. Entropy
        features["hostname_entropy"] = calculate_entropy(hostname)
        features["path_entropy"] = calculate_entropy(path)
        
        features["scheme"] = parsed.scheme
        features["hostname"] = hostname
        features["tld"] = tld
        
        return features
