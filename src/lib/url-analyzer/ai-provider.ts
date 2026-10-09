import { GoogleGenerativeAI } from '@google/generative-ai';
import { ParsedUrlFeatures } from './parser';
import { RuleAnalysisResult } from './rule-engine';

export interface AiAnalysisResult {
  verdict: "SAFE" | "SUSPICIOUS" | "PHISHING" | "UNKNOWN";
  confidence: number;
  riskScore: number;
  riskLevel: "SAFE" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  riskFactors: {
    type: string;
    severity: string;
    title: string;
    explanation: string;
  }[];
  summary: string;
  recommendation: string;
  aiReasoning: string;
}

export async function analyzeUrlWithGemini(
  url: string,
  parsedFeatures: ParsedUrlFeatures,
  ruleAnalysis: RuleAnalysisResult
): Promise<AiAnalysisResult | null> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.warn("GEMINI_API_KEY is not set.");
    return null;
  }

  const genAI = new GoogleGenerativeAI(apiKey);
  const model = genAI.getGenerativeModel({
    model: "gemini-3.6-flash",
    generationConfig: {
      responseMimeType: "application/json",
    }
  });

  const prompt = `You are CyberGuard's cybersecurity URL analysis engine.
Your task is to analyze a URL for potential phishing, impersonation, malicious behavior, or suspicious characteristics.

The backend has already parsed the URL and generated deterministic security signals.
Treat the backend URL parser as authoritative. Do NOT invent URL parsing values.

Original URL: ${url}
Parsed Features: ${JSON.stringify(parsedFeatures)}
Rule Engine Score: ${ruleAnalysis.score}
Rule Findings: ${JSON.stringify(ruleAnalysis.findings)}

Analyze the security implications of these features.
Pay particular attention to:
- brand impersonation
- domain mismatch
- suspicious subdomains
- suspicious keywords
- IP-based URLs
- unusual ports
- URL shortening
- encoding/obfuscation
- social engineering indicators

Do NOT declare a URL phishing based on a single weak signal.

Return ONLY valid JSON.
Require Gemini to return structured JSON exactly matching this schema:
{
  "verdict": "SAFE" | "SUSPICIOUS" | "PHISHING" | "UNKNOWN",
  "confidence": number (0-100),
  "riskScore": number (0-100),
  "riskLevel": "SAFE" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  "riskFactors": [
    {
      "type": "string (e.g., BRAND_IMPERSONATION)",
      "severity": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
      "title": "string",
      "explanation": "string"
    }
  ],
  "summary": "string",
  "recommendation": "string",
  "aiReasoning": "string"
}`;

  try {
    const result = await model.generateContent(prompt);
    const text = result.response.text();
    const jsonStr = text.replace(/^```json\\s*/, '').replace(/\\s*```$/, '');
    const data = JSON.parse(jsonStr) as AiAnalysisResult;
    
    // Basic validation
    if (!data.verdict || typeof data.riskScore !== 'number') {
      return null;
    }
    return data;
  } catch (error) {
    console.error("Gemini API Error:", error);
    return null;
  }
}
