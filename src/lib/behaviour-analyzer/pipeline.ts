import { GoogleGenerativeAI } from '@google/generative-ai';

export async function runBehaviourPipeline(userId: string, events: any[]) {
  let ruleScore = 0;
  const indicators: string[] = [];
  
  const failedLogins = events.filter(e => e.type === "LOGIN_FAILED").length;
  if (failedLogins >= 3) {
    ruleScore += 40;
    indicators.push("MULTIPLE_FAILED_LOGINS");
  }

  const locations = new Set(events.map(e => e.location));
  if (locations.size > 2) {
    ruleScore += 30;
    indicators.push("IMPOSSIBLE_TRAVEL");
  }

  // AI Reasoning (Removed - reverted to pure rules)
  let aiAnalysis: any = null;
  
  // Merge
  let finalScore = Math.min(100, ruleScore);
  let riskLevel = finalScore >= 80 ? "CRITICAL" : finalScore > 40 ? "HIGH" : "SAFE";
  let summary = "Rule-based analysis applied.";
  let recommendedAction = "Proceed normally.";
  let riskFactors = indicators.map(ind => ({ type: ind, severity: "HIGH", title: ind, explanation: "Detected by rule engine" }));

  if (aiAnalysis) {
    finalScore = Math.round((finalScore * 0.6) + (aiAnalysis.riskScore * 0.4));
    riskLevel = aiAnalysis.riskLevel;
    summary = aiAnalysis.summary;
    recommendedAction = aiAnalysis.recommendedAction;
    riskFactors = [...riskFactors, ...aiAnalysis.riskFactors];
  }

  return {
    verdict: finalScore > 70 ? "MALICIOUS" : finalScore > 40 ? "SUSPICIOUS" : "SAFE",
    riskScore: finalScore,
    riskLevel,
    confidence: aiAnalysis ? aiAnalysis.confidence : 75,
    riskFactors,
    explanation: summary,
    recommendation: recommendedAction,
    aiStatus: aiAnalysis ? "SUCCESS" : "UNAVAILABLE"
  };
}
