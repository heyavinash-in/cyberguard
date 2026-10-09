import { NextRequest, NextResponse } from 'next/server';
import { runImpersonationPipeline } from '@/lib/impersonation-analyzer/pipeline';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { claimedIdentity, message, sender } = body;

    if (!message || !claimedIdentity) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_INPUT', message: 'Missing fields.' } },
        { status: 400 }
      );
    }

    const result = await runImpersonationPipeline(claimedIdentity, message, sender);
    
    return NextResponse.json({
      success: true,
      data: result,
      meta: {
        aiUsed: result.aiStatus === 'SUCCESS',
        analysisVersion: '1.0'
      }
    });
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: { code: 'SERVER_ERROR', message: error.message } },
      { status: 500 }
    );
  }
}
