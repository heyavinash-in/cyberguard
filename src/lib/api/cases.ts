const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface ThreatCaseSummary {
  id: string;
  timestamp: string;
  engine: string;
  classification: string;
  risk_score: number;
  risk_level: string;
  status: string;
}

export interface ThreatCaseDetail extends ThreatCaseSummary {
  event_id: string;
  summary: string;
  raw_result: any;
}

export async function getCases(): Promise<{ items: ThreatCaseSummary[] }> {
  const res = await fetch(`${API_BASE}/api/v1/cases`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch cases");
  return res.json();
}

export async function getCase(caseId: string): Promise<ThreatCaseDetail> {
  const res = await fetch(`${API_BASE}/api/v1/cases/${caseId}`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch case detail");
  return res.json();
}
