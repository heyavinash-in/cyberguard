import { NextRequest, NextResponse } from 'next/server';
import { runUrlAnalysisPipeline } from '@/lib/url-analyzer/pipeline';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { url } = body;

    if (!url || typeof url !== 'string' || url.length > 2048) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_INPUT', message: 'Valid URL is required.' } },
        { status: 400 }
      );
    }

    const result = await runUrlAnalysisPipeline(url);
    
    // The backend now completely drives the response.
    return NextResponse.json({
      success: true,
      data: {
        verdict: result.classification.label,
        riskScore: result.classification.risk_score,
        riskLevel: result.classification.severity,
        confidence: result.classification.confidence * 100,
        urlFeatures: result.features,
        riskFactors: result.findings,
        summary: result.summary,
        recommendation: result.recommended_actions.join(" "),
        mlStatus: "SUCCESS"
      },
      meta: {
        mlUsed: true,
        analysisVersion: result.engine.version
      }
    });
  } catch (error: any) {
    console.error('URL Analysis Error:', error);
    return NextResponse.json(
      { success: false, error: { code: 'SERVER_ERROR', message: error.message || 'Analysis failed.' } },
      { status: 500 }
    );
  }
}
