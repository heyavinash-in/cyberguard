import { NextRequest, NextResponse } from 'next/server';
import { runMessageAnalysisPipeline } from '@/lib/message-analyzer/pipeline';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { message, sender } = body;

    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_INPUT', message: 'Message is required.' } },
        { status: 400 }
      );
    }

    const result = await runMessageAnalysisPipeline(message, sender);
    
    return NextResponse.json({
      success: true,
      data: result,
      meta: {
        mlUsed: result.mlStatus === 'SUCCESS',
        analysisVersion: '1.0'
      }
    });
  } catch (error: any) {
    console.error('Message Analysis Error:', error);
    return NextResponse.json(
      { success: false, error: { code: 'SERVER_ERROR', message: error.message || 'Analysis failed.' } },
      { status: 500 }
    );
  }
}
