import re
import math
from urllib.parse import urlparse

try:
    import tldextract
except ImportError:
    tldextract = None

def calculate_entropy(text):
    if not text:
        return 0
    entropy = 0
    for x in set(text):
        p_x = float(text.count(x)) / len(text)
        entropy += - p_x * math.log2(p_x)
    return entropy

class URLFeatureExtractor:
    def __init__(self):
        self.suspicious_words = {
            'login', 'verify', 'update', 'secure', 'account', 'bank', 
            'signin', 'auth', 'confirm', 'billing', 'support',
            'service', 'recover', 'wallet', 'crypto', 'free', 'bonus'
        }
        self.brands = ['paypal', 'microsoft', 'google', 'apple', 'amazon', 'netflix', 'facebook', 'instagram', 'chase', 'wellsfargo']
        self.shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'is.gd', 'cli.gs', 'yfrog.com', 'ow.ly', 'deck.ly', 't.cn']
        self.unusual_tlds = ['xyz', 'top', 'cc', 'tk', 'gq', 'cf', 'pw', 'info', 'biz', 'vip', 'club', 'online', 'site', 'ru', 'cn']
        self.download_exts = ['.exe', '.zip', '.scr', '.apk', '.rar', '.bat', '.cmd', '.msi', '.bin']

    def extract_features(self, url: str) -> dict:
        if not url.startswith('http'):
            url = 'http://' + url
            
        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        path = parsed.path or ''
        
        is_ip = 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) else 0
        
        domain = hostname
        subdomain = ''
        tld = ''
        
        if tldextract and not is_ip:
            ext = tldextract.extract(url)
            domain = ext.domain
            subdomain = ext.subdomain
            tld = ext.suffix

        num_subdomains = subdomain.count('.') + 1 if subdomain else 0
        
        # Subdomain Manipulation: check if subdomain looks like a real domain
        # e.g. paypal.com.security-check.in -> subdomain is paypal.com
        subdomain_manipulation = 0
        if subdomain:
            for brand in self.brands:
                if brand in subdomain.lower() and domain.lower() != brand:
                    subdomain_manipulation = 1
                    break
        
        # Brand Impersonation / Typosquatting
        impersonation = 0
        impersonated_brand = None
        if not is_ip:
            stripped_domain = domain.lower().replace('-', '')
            for brand in self.brands:
                # If the true brand string is hidden inside the domain (e.g. net-flix -> netflix)
                if brand in stripped_domain and domain.lower() != brand:
                    impersonation = 1
                    impersonated_brand = brand
                    break
                
                # Simple typosquatting check (replacing o with 0, i with 1, etc)
                typo_brand = brand.replace('o', '0').replace('i', '1').replace('e', '3').replace('a', '4')
                if typo_brand in domain.lower() and typo_brand != brand:
                    impersonation = 1
                    impersonated_brand = brand
                    break

        # Unusual TLD
        has_unusual_tld = 1 if tld.lower() in self.unusual_tlds else 0
        
        # Shortened URL
        is_shortened = 1 if domain.lower() + '.' + tld.lower() in self.shorteners or hostname.lower() in self.shorteners else 0
        
        # Direct Download Trigger
        is_direct_download = 0
        for ext in self.download_exts:
            if path.lower().endswith(ext):
                is_direct_download = 1
                break

        url_lower = url.lower()
        has_suspicious = 1 if any(word in url_lower for word in self.suspicious_words) else 0

        is_legit_brand = 1 if domain.lower() in self.brands else 0
        
        features = {
            'is_https': 1 if parsed.scheme == 'https' else 0,
            'is_ip_address': is_ip,
            'num_subdomains': num_subdomains,
            'has_suspicious_words': has_suspicious,
            'subdomain_manipulation': subdomain_manipulation,
            'impersonation': impersonation,
            'impersonated_brand': impersonated_brand,
            'has_unusual_tld': has_unusual_tld,
            'tld': tld,
            'is_shortened': is_shortened,
            'is_direct_download': is_direct_download,
            'is_legit_brand': is_legit_brand,
            'download_ext': path.split('.')[-1] if is_direct_download else None
        }
        
        return features

    def extract_vector(self, url: str) -> list:
        # No longer used by ML, but kept to prevent import errors just in case
        return []
