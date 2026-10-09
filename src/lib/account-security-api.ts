export interface AccountActivityRequest {
  user_id: string;
  timestamp: string;
  ip_address: string;
  country: string;
  city?: string;
  device_id: string;
  device_type: string;
  login_success: boolean;
  failed_login_count: number;
  mfa_used: boolean;
  mfa_configuration_changed: boolean;
  session_id: string;
  active_session_count: number;
  vpn_detected: boolean;
  event_description?: string;
}

export interface Finding {
  finding_id: string;
  category: string;
  severity: string;
  title: string;
  explanation: string;
  evidence: string;
  contribution: number;
}

export interface TimelineEvent {
  timestamp: string;
  event: string;
  description: string;
}

export interface AccountActivityResponse {
  request_id: string;
  user_id: string;
  risk_score: number;
  risk_level: string;
  classification: string;
  confidence: number;
  explanation: string;
  baseline_comparison: Record<string, string>;
  findings: Finding[];
  correlations: any[];
  timeline: TimelineEvent[];
  recommended_actions: string[];
  model_info: Record<string, string>;
  processing: Record<string, number>;
}

export async function analyzeAccountActivity(request: AccountActivityRequest): Promise<AccountActivityResponse> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  
  const response = await fetch(`${baseUrl}/api/v1/account/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(request)
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}
