import { NextRequest, NextResponse } from 'next/server';
import { runBehaviourPipeline } from '@/lib/behaviour-analyzer/pipeline';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { userId, events } = body;

    if (!userId || !events) {
      return NextResponse.json(
        { success: false, error: { code: 'INVALID_INPUT', message: 'Missing fields.' } },
        { status: 400 }
      );
    }

    const result = await runBehaviourPipeline(userId, events);
    
    return NextResponse.json({
      success: true,
      data: result,
      meta: { aiUsed: result.aiStatus === 'SUCCESS', analysisVersion: '1.0' }
    });
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: { code: 'SERVER_ERROR', message: error.message } },
      { status: 500 }
    );
  }
}
