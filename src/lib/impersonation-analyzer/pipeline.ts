import { GoogleGenerativeAI } from '@google/generative-ai';

export async function runImpersonationPipeline(claimedIdentity: string, message: string, sender: string) {
  // Deterministic rule checks
  let ruleScore = 0;
  const indicators: string[] = [];
  
  const senderLower = sender.toLowerCase();
  const identityLower = claimedIdentity.toLowerCase();
  const msgLower = message.toLowerCase();

  // Rule 1: Freemail checking for authorities
  const freemail = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"];
  const isAuthority = ["admin", "university", "bank", "police", "manager", "ceo"].some(k => identityLower.includes(k));
  
  if (isAuthority && freemail.some(domain => senderLower.includes(domain))) {
    ruleScore += 40;
    indicators.push("AUTHORITY_USING_FREEMAIL");
  }

  // Rule 2: Identity mismatch
  if (identityLower && senderLower && !senderLower.includes(identityLower.split(' ')[0])) {
    ruleScore += 20;
    indicators.push("SENDER_IDENTITY_MISMATCH");
  }

  // Rule 3: Requests for secrecy or urgency
  if (/(don't tell|secret|urgent|immediately|fired|suspended)/.test(msgLower)) {
    ruleScore += 25;
    indicators.push("URGENCY_OR_SECRECY");
  }

  // AI Reasoning (Removed - reverted to pure rules)
  let aiAnalysis: any = null;
  
  // Merge
  let finalScore = Math.min(100, ruleScore);
  let finalVerdict = finalScore > 70 ? "MALICIOUS" : finalScore > 40 ? "SUSPICIOUS" : "SAFE";
  let finalConfidence = 70;
  let riskLevel = finalScore > 70 ? "HIGH" : "LOW";
  let summary = "Rule-based analysis applied.";
  let recommendedAction = "Proceed with caution.";
  let riskFactors = indicators.map(ind => ({ type: ind, severity: "MEDIUM", title: ind, explanation: "Detected by rule engine" }));

  if (aiAnalysis) {
    finalScore = Math.round((finalScore * 0.5) + (aiAnalysis.riskScore * 0.5));
    finalVerdict = aiAnalysis.verdict;
    finalConfidence = aiAnalysis.confidence;
    riskLevel = aiAnalysis.riskLevel;
    summary = aiAnalysis.summary;
    recommendedAction = aiAnalysis.recommendedAction;
    riskFactors = [...riskFactors, ...aiAnalysis.riskFactors];
  }

  return {
    verdict: finalVerdict,
    riskScore: finalScore,
    riskLevel,
    confidence: finalConfidence,
    riskFactors,
    explanation: summary,
    recommendation: recommendedAction,
    aiStatus: aiAnalysis ? "SUCCESS" : "UNAVAILABLE"
  };
}
