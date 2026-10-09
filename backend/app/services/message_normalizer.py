import re
import unicodedata
from typing import Dict, Any, Tuple

# Security term lexicon for conservative normalization
SECURITY_LEXICON = {
    'credential', 'credentials', 'password', 'passcode', 'username', 'login', 'signin', 'account',
    'verify', 'verification', 'otp', 'code', 'auth', 'authenticate', 'token', 'security',
    'payment', 'bank', 'banking', 'transfer', 'wire', 'invoice', 'refund', 'wallet', 'crypto',
    'suspend', 'suspended', 'lock', 'locked', 'restrict', 'restricted', 'block', 'blocked', 'closed',
    'reward', 'prize', 'lottery', 'gift', 'claim',
    'support', 'admin', 'administrator', 'system', 'update', 'urgent', 'immediately',
    'never', 'anyone', 'strangers', 'do', 'not', 'dont', 'provide', 'share', 'tell', 'send', 'confirm', 'enter', 'submit'
}

# Cyrillic to Latin homoglyph mapping (partial)
HOMOGLYPHS = {
    'а': 'a', 'с': 'c', 'е': 'e', 'о': 'o', 'р': 'p', 'х': 'x', 'у': 'y'
}

def remove_homoglyphs(text: str) -> str:
    res = []
    for char in text:
        res.append(HOMOGLYPHS.get(char, char))
    return ''.join(res)

def normalize_leetspeak(word: str) -> str:
    # Conservative leetspeak translation
    # 0->o, 1->i, 3->e, 4->a, 5->s, 7->t, @->a
    trans = str.maketrans('013457@', 'oieasta')
    return word.translate(trans)

def normalize_message(text: str) -> Tuple[str, list]:
    findings = []
    
    # 1. Unicode normalization (NFKC)
    norm_text = unicodedata.normalize('NFKC', text)
    
    # 2. Homoglyphs
    homo_text = remove_homoglyphs(norm_text)
    if homo_text != norm_text:
        findings.append("unicode_homoglyphs")
    current_text = homo_text
    
    # 3. Spaced-out words (e.g., s e n d  m e  y o u r  p a s s w o r d)
    # Detect patterns of single letters separated by spaces.
    def space_replacer(match):
        condensed = match.group(0).replace(' ', '')
        return condensed
        
    spaced_pattern = r'(?:[a-zA-Z]\s){3,}[a-zA-Z]'
    if re.search(spaced_pattern, current_text):
        findings.append("spaced_out_words")
        current_text = re.sub(spaced_pattern, space_replacer, current_text)
        
    # 4. Punctuation/Hyphen fragmentation
    # p-a-s-s-w-o-r-d, A-ccount, S-uspended
    # We look for a letter, a punctuation [!_.-], and then more letters.
    # We don't want to break "COVID-19" or "e-commerce".
    # We will compress sequences like a-b-c-d or A-ccount and check if they form a dictionary word,
    # or just unconditionally compress them if they match an aggressive fragmentation pattern.
    
    # Pattern A: p.a.s.s.w.o.r.d (multiple separated characters)
    def punct_replacer_agg(match):
        return re.sub(r'[!_.-]', '', match.group(0))
        
    frag_pattern = r'(?:[a-zA-Z][!_.-]){2,}[a-zA-Z]'
    if re.search(frag_pattern, current_text):
        if "fragmentation" not in findings: findings.append("punctuation_fragmentation")
        current_text = re.sub(frag_pattern, punct_replacer_agg, current_text)
        
    # Pattern B: A-ccount, S-uspended (Capital letter, hyphen/punct, rest of word)
    def prefix_frag_replacer(match):
        return match.group(1) + match.group(2)
        
    prefix_frag = r'\b([a-zA-Z])[!_.-]+([a-zA-Z]{4,})\b'
    if re.search(prefix_frag, current_text):
        if "fragmentation" not in findings: findings.append("hyphen_fragmentation")
        current_text = re.sub(prefix_frag, prefix_frag_replacer, current_text)

    # 5. Leetspeak
    # Check words that mix letters and numbers, or purely numbers that might translate to a security word
    words = current_text.split()
    new_words = []
    has_leet = False
    for w in words:
        w_lower = w.lower()
        if any(c.isdigit() or c == '@' for c in w_lower):
            leeted = normalize_leetspeak(w_lower)
            # Remove trailing punctuation for lexicon check
            clean_leeted = re.sub(r'\W+', '', leeted)
            if clean_leeted in SECURITY_LEXICON:
                new_words.append(leeted) # preserve original punctuation but leet-translated
                has_leet = True
                continue
        new_words.append(w)
        
    if has_leet:
        findings.append("leetspeak")
        current_text = ' '.join(new_words)
        
    # Standard lowercase normalization
    normalized_text = current_text.lower()
    
    # 6. Compound Security Terms Normalization
    compounds = {
        r'\bpass[\s\-_]+code\b': 'passcode',
        r'\bverification[\s\-_]+code\b': 'verification_code',
        r'\bsecurity[\s\-_]+code\b': 'security_code',
        r'\brecovery[\s\-_]+code\b': 'recovery_code',
        r'\bauth[\s\-_]+code\b': 'auth_code',
        r'\bauthentication[\s\-_]+code\b': 'authentication_code',
        r'\bone[\s\-_]+time[\s\-_]+password\b': 'otp',
        r'\bone[\s\-_]+time[\s\-_]+passcode\b': 'otp'
    }
    for pattern, replacement in compounds.items():
        normalized_text = re.sub(pattern, replacement, normalized_text)
    
    return normalized_text, findings

if __name__ == "__main__":
    tests = [
        "Your A-ccount will be S-uspended",
        "S e n d m e y o u r p a s s w o r d",
        "v3rify y0ur 0tp",
        "p.a.s.s.w.o.r.d",
        "e-commerce is well-known",
        "hello how are you"
    ]
    for t in tests:
        n, f = normalize_message(t)
        print(f"Original: {t}")
        print(f"Norm: {n}")
        print(f"Findings: {f}\n")
