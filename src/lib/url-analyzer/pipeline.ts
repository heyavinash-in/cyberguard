export interface FinalAnalysisResult {
  success: boolean;
  input: {
    original_url: string;
    normalized_url: string;
  };
  classification: {
    label: string;
    severity: string;
    risk_score: number;
    confidence: number;
  };
  summary: string;
  findings: any[];
  features: any;
  model: any;
  risk: {
    score: number;
    severity: string;
    confidence: number;
  };
  recommended_actions: string[];
  engine: any;
}

export async function runUrlAnalysisPipeline(url: string): Promise<FinalAnalysisResult> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
  
  try {
    const response = await fetch(`${baseUrl}/api/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Local ML service unavailable:", error);
    throw error;
  }
}
