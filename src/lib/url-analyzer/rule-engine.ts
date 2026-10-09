import { ParsedUrlFeatures } from './parser';

export interface RuleFinding {
  type: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  title: string;
  explanation: string;
  scoreContribution: number;
}

export interface RuleAnalysisResult {
  score: number;
  findings: RuleFinding[];
}

export function analyzeUrlRules(url: string, features: ParsedUrlFeatures): RuleAnalysisResult {
  let score = 0;
  const findings: RuleFinding[] = [];

  const addFinding = (finding: RuleFinding) => {
    findings.push(finding);
    score += finding.scoreContribution;
  };

  // A. IP Address Check
  if (features.isIpAddress) {
    addFinding({
      type: "IP_ADDRESS",
      severity: "HIGH",
      title: "Direct IP Address Usage",
      explanation: "URL uses a raw IP address instead of a domain name, which is highly unusual for legitimate services and often indicates phishing or malware hosting.",
      scoreContribution: 35
    });
  }

  // B. Protocol Check
  if (features.protocol === "http" && !features.hostname.includes("localhost")) {
    addFinding({
      type: "INSECURE_PROTOCOL",
      severity: "MEDIUM",
      title: "Unencrypted HTTP Connection",
      explanation: "URL does not use HTTPS. Any data transmitted can be intercepted.",
      scoreContribution: 10
    });
  }

  // C. Excessive Subdomains
  const subdomainParts = features.subdomain.split(".").filter(Boolean);
  if (subdomainParts.length > 2) {
    addFinding({
      type: "EXCESSIVE_SUBDOMAINS",
      severity: "MEDIUM",
      title: "Excessive Subdomains",
      explanation: "URL uses deeply nested subdomains, a common technique to obscure the true registrable domain.",
      scoreContribution: 15
    });
  }

  // D. Brand Impersonation / Domain Mismatch
  const knownBrands = ["google", "paypal", "microsoft", "apple", "amazon", "netflix", "facebook", "bank", "login", "secure", "account", "verify"];
  const subdomainHasBrand = knownBrands.some(brand => features.subdomain.includes(brand));
  const domainHasBrand = knownBrands.some(brand => features.registrableDomain.includes(brand));

  if (subdomainHasBrand && !domainHasBrand) {
    addFinding({
      type: "BRAND_MISMATCH",
      severity: "CRITICAL",
      title: "Brand Impersonation in Subdomain",
      explanation: `A recognizable brand or security keyword appears in the subdomain, but the actual registrable domain (${features.registrableDomain}) belongs to someone else. This is a classic phishing technique.`,
      scoreContribution: 40
    });
  }

  // E. Suspicious URL Keywords
  const suspiciousKeywords = ["login", "verify", "verification", "secure", "security", "account", "update", "confirm", "password", "wallet", "payment", "signin", "authenticate"];
  const urlLower = url.toLowerCase();
  
  // Only check path/query for keywords so we don't double penalize the brand check
  const pathQuery = (features.pathname + features.query).toLowerCase();
  let keywordMatchCount = 0;
  for (const kw of suspiciousKeywords) {
    if (pathQuery.includes(kw)) {
      keywordMatchCount++;
    }
  }

  if (keywordMatchCount > 0) {
    addFinding({
      type: "SUSPICIOUS_KEYWORDS",
      severity: "LOW",
      title: "Suspicious Path Keywords",
      explanation: `URL contains keywords often associated with credential harvesting (e.g., login, verify, account).`,
      scoreContribution: Math.min(15, keywordMatchCount * 5)
    });
  }

  // F. Suspicious Characters/Encoding
  if (url.includes("%40") || url.includes("@")) {
    addFinding({
      type: "OBFUSCATION",
      severity: "HIGH",
      title: "URL Obfuscation",
      explanation: "Contains an '@' symbol, which can be used to hide the true destination domain by passing credentials in the URL structure.",
      scoreContribution: 25
    });
  }

  // G. URL Length
  if (url.length > 150) {
    addFinding({
      type: "EXCESSIVE_LENGTH",
      severity: "LOW",
      title: "Unusually Long URL",
      explanation: "The URL is excessively long, potentially attempting to hide malicious parameters or overflow the address bar.",
      scoreContribution: 5
    });
  }

  // H. Suspicious Port
  const safePorts = ["80", "443", "8080", "3000"];
  if (!safePorts.includes(features.port)) {
    addFinding({
      type: "UNUSUAL_PORT",
      severity: "MEDIUM",
      title: "Unusual Port",
      explanation: `URL connects to an unusual port (${features.port}) which is irregular for standard web traffic.`,
      scoreContribution: 10
    });
  }

  // I. URL Shorteners
  const shorteners = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly"];
  if (shorteners.some(s => features.registrableDomain === s)) {
    addFinding({
      type: "URL_SHORTENER",
      severity: "MEDIUM",
      title: "URL Shortener Used",
      explanation: "URL obscures the final destination using a link shortener.",
      scoreContribution: 15
    });
  }

  return {
    score: Math.min(100, Math.max(0, score)),
    findings
  };
}
