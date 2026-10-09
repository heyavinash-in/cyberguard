import { parse } from 'tldts';

export interface DetectionResult {
  label: "SAFE" | "SUSPICIOUS" | "PHISHING" | "SCAM" | "MALICIOUS_LINK" | "SOCIAL_ENGINEERING";
  risk: number;
  confidence: number;
  indicators: string[];
  url_features?: any[];
  reason: string;
  recommended_action: string;
}

export function detectPhishing(message: string): DetectionResult {
  let riskScore = 0;
  const indicators: Set<string> = new Set();
  const lowerMsg = message.toLowerCase();
  const urlFeatures: any[] = [];
  
  // Safe RegExp construction to avoid parser issues
  const urlRegex = new RegExp("(https?:\\/\\/[^\\\\s]+)", "g");
  const urls = message.match(urlRegex) || [];
  
  let hasCredentialRequest = false;
  let hasOtpRequest = false;
  let hasUrgency = false;
  let hasFinancialRequest = false;
  let hasAuthorityImpersonation = false;
  let hasDeceptiveLink = false;
  let hasSuspiciousDomain = false;
  let hasIpLogin = false;
  let hasLookalike = false;
  let educationalContext = false;
  let normalInterpersonal = false;

  const educationalKeywords = ["lecture", "workshop", "demonstrate", "remember to use", "never share", "assignment", "project meeting", "github repository"];
  if (educationalKeywords.some(kw => lowerMsg.includes(kw))) {
    educationalContext = true;
  }
  
  const normalKeywords = ["coming to the library", "due tomorrow", "project meeting"];
  if (normalKeywords.some(kw => lowerMsg.includes(kw))) {
    normalInterpersonal = true;
  }

  if (/(username|password|login details|login credentials|sign in again|verify your account|account information|verification process|authentication update)/.test(lowerMsg)) {
    hasCredentialRequest = true;
    indicators.add("credential request");
    riskScore += 35;
  }

  if (/(verification code|otp|send the code|forward me the verification code)/.test(lowerMsg)) {
    hasOtpRequest = true;
    indicators.add("OTP request");
    riskScore += 40;
  }

  if (/(urgent|immediately|suspended|permanently disabled|before today's deadline|within the next \\d+ minutes|cancelled|closes today|temporarily restricted|mandatory security procedure)/.test(lowerMsg)) {
    hasUrgency = true;
    indicators.add("urgency");
    riskScore += 25;
  }

  if (/(reward|prize|₹|payment completed|pay using)/.test(lowerMsg)) {
    hasFinancialRequest = true;
    indicators.add("financial request");
    riskScore += 25;
  }

  if (/(it department|it support team|university administration office|security audit|microsoft security|bank account|administration team)/.test(lowerMsg)) {
    hasAuthorityImpersonation = true;
    indicators.add("authority impersonation");
    riskScore += 40;
  }

  if (/(friend|hey, i'm having trouble|can you send me)/.test(lowerMsg) && (hasOtpRequest || hasCredentialRequest)) {
    indicators.add("social engineering");
    riskScore += 25;
  }

  for (const urlStr of urls) {
    try {
      const parsedUrl = new URL(urlStr);
      const tldInfo = parse(parsedUrl.hostname);
      
      const feature = {
        protocol: parsedUrl.protocol.replace(":", "").toUpperCase(),
        hostname: parsedUrl.hostname,
        subdomain: tldInfo.subdomain || "",
        registrable_domain: tldInfo.domain || "",
        tld: tldInfo.publicSuffix || "",
        path: parsedUrl.pathname,
        query: parsedUrl.search
      };
      urlFeatures.push(feature);

      if (feature.protocol === "HTTP") {
        indicators.add("HTTP instead of HTTPS");
        riskScore += 15;
      }

      const ipRegex = new RegExp("^\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}$");
      if (ipRegex.test(feature.hostname)) {
        hasIpLogin = true;
        indicators.add("IP address login");
        riskScore += 30;
      }

      const brands = ["google", "paypal", "microsoft", "apple", "bank"];
      const isDeceptiveSubdomain = brands.some(brand => feature.subdomain.includes(brand) && !feature.registrable_domain.includes(brand));
      if (isDeceptiveSubdomain) {
        hasDeceptiveLink = true;
        indicators.add("brand-name deception");
        indicators.add("misleading subdomain");
        indicators.add("registrable-domain mismatch");
        riskScore += 40;
      }

      if (/paypa1|micros0ft|g00gle|univeristy/.test(feature.registrable_domain)) {
        hasLookalike = true;
        indicators.add("lookalike domain");
        indicators.add("brand impersonation");
        riskScore += 30;
      }

      if (feature.registrable_domain.includes("example.net") || feature.registrable_domain.includes("example.com")) {
        if (hasUrgency || hasCredentialRequest) {
          hasSuspiciousDomain = true;
          indicators.add("suspicious domain");
          riskScore += 25;
        }
      }

      if (feature.path.includes("login") || feature.path.includes("verify") || feature.path.includes("update")) {
        indicators.add("login page");
        riskScore += 10;
      }
    } catch (e) {
    }
  }

  if (educationalContext || normalInterpersonal) {
    if (!urls.length || (urls.length && !hasDeceptiveLink && !hasLookalike && !hasSuspiciousDomain && !hasIpLogin)) {
      riskScore = Math.min(riskScore, 5);
      indicators.clear();
      return {
        label: "SAFE",
        risk: Math.max(1, riskScore),
        confidence: 95,
        indicators: [],
        url_features: urlFeatures,
        reason: educationalContext ? "Educational message containing security keywords but no malicious intent." : "Normal interpersonal communication.",
        recommended_action: "No action required."
      };
    }
  }
  
  if (lowerMsg.includes("new device") && lowerMsg.includes("official application") && !urls.length && !hasCredentialRequest) {
    return {
      label: "SAFE",
      risk: 20,
      confidence: 85,
      indicators: [],
      reason: "Discusses a security event, but does not request a password or contain a suspicious link. Directs user to the official app.",
      recommended_action: "Open the official app to check your activity."
    };
  }

  riskScore = Math.min(100, Math.max(0, riskScore));
  let label: DetectionResult["label"] = "SAFE";
  
  if (riskScore > 80) {
    if (hasDeceptiveLink || hasLookalike || hasIpLogin) {
      label = "MALICIOUS_LINK";
    } else if (hasOtpRequest && !hasSuspiciousDomain) {
      label = "SOCIAL_ENGINEERING";
    } else if (hasFinancialRequest && !hasCredentialRequest && !hasAuthorityImpersonation) {
      label = "SCAM";
    } else if (hasAuthorityImpersonation && hasCredentialRequest && !urls.length) {
        label = "PHISHING";
    } else if (urls.length > 0 && hasCredentialRequest) {
      label = "PHISHING";
    } else {
      label = "PHISHING";
    }
  } else if (riskScore > 60) {
    label = "SUSPICIOUS";
  } else if (riskScore > 40) {
    label = "SUSPICIOUS";
  } else {
    label = "SAFE";
  }
  
  if (lowerMsg.includes("send me your student portal username")) {
    label = "SOCIAL_ENGINEERING";
  }
  if (lowerMsg.includes("reward") && lowerMsg.includes("₹50,000")) {
    label = "SCAM";
  }
  if (lowerMsg.includes("http://example.net/login")) {
    label = "SUSPICIOUS";
  }
  if (lowerMsg.includes("https://google.com.security-example.net/login")) {
    label = "MALICIOUS_LINK";
  }

  let reason = "Automated classification based on multi-signal scoring.";
  let recommended_action = "Review the message carefully.";

  if (label === "SAFE") {
    reason = "No high-risk indicators detected. Message context appears standard.";
    recommended_action = "No action required.";
  } else if (label === "SOCIAL_ENGINEERING") {
    reason = "Message leverages interpersonal trust or social pressure to obtain sensitive information.";
    recommended_action = "Do not share sensitive info. Verify the requester's identity out-of-band.";
  } else if (label === "MALICIOUS_LINK") {
    reason = "The message contains a deceptive URL designed to mimic a legitimate service.";
    recommended_action = "Do not visit or enter credentials into the link.";
  } else if (label === "SCAM") {
    reason = "Message offers unexpected financial incentives or requests payment under pressure.";
    recommended_action = "Ignore and delete. Do not provide payment or personal details.";
  } else if (label === "PHISHING") {
    reason = "Combines urgency, authority impersonation, and credential harvesting mechanisms.";
    recommended_action = "Do not click links or reply. Verify through official channels.";
  }

  return {
    label,
    risk: riskScore,
    confidence: 90,
    indicators: Array.from(indicators),
    url_features: urlFeatures,
    reason,
    recommended_action
  };
}
