import { detectPhishing } from '../phishing-detector';
import { GoogleGenerativeAI } from '@google/generative-ai';

export async function runMessageAnalysisPipeline(message: string, sender: string = "") {
  // We completely rely on the backend now.
  let backendResult = null;
  try {
    const response = await fetch("http://localhost:8000/api/analyze/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message, sender: sender })
    });
    if (response.ok) {
      backendResult = await response.json();
    } else {
      throw new Error(`Backend returned ${response.status}`);
    }
  } catch (error) {
    console.error("Local ML service unavailable:", error);
    // Fallback if backend is down
    return {
      verdict: "SAFE",
      riskScore: 0,
      riskLevel: "SAFE",
      confidence: 0,
      riskFactors: [],
      explanation: "Backend offline.",
      recommendation: "",
      mlStatus: "UNAVAILABLE"
    };
  }
  
  // Transform backend result to frontend structure
  const combinedRiskFactors = backendResult.findings.map((f: any) => ({
    type: f.category,
    severity: f.severity,
    title: f.message,
    explanation: f.source
  }));

  return {
    verdict: backendResult.classification,
    riskScore: backendResult.risk_score,
    riskLevel: backendResult.severity,
    confidence: backendResult.confidence,
    riskFactors: combinedRiskFactors,
    explanation: backendResult.severity === "SAFE" ? "Message appears safe." : "Message flagged for social engineering indicators.",
    recommendation: backendResult.recommended_response.join(" "),
    mlStatus: "SUCCESS"
  };
}

function determineRiskLevel(score: number): string {
  if (score < 20) return "SAFE";
  if (score < 40) return "LOW";
  if (score < 60) return "MEDIUM";
  if (score < 80) return "HIGH";
  return "CRITICAL";
}
