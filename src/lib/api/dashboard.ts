const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface DashboardSummary {
  threats_detected: number;
  critical_threats: number;
  scans_analyzed: number;
  active_cases: number;
  last_updated: string | null;
}

export interface EngineStats {
  id: string;
  name: string;
  status: string;
  total_scans: number;
  threats_detected: number;
  last_activity: string | null;
}

export interface DashboardActivity {
  id: string;
  timestamp: string;
  engine: string;
  event_type: string;
  title: string;
  risk_score: number;
  risk_level: string;
  classification: string;
}

export interface RiskDistribution {
  safe: number;
  low: number;
  medium: number;
  high: number;
  critical: number;
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const res = await fetch(`${API_BASE}/api/v1/dashboard/summary`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch dashboard summary");
  return res.json();
}

export async function getDashboardEngines(): Promise<{ engines: EngineStats[] }> {
  const res = await fetch(`${API_BASE}/api/v1/dashboard/engines`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch engines stats");
  return res.json();
}

export async function getDashboardActivity(limit: number = 10): Promise<{ items: DashboardActivity[] }> {
  const res = await fetch(`${API_BASE}/api/v1/dashboard/activity?limit=${limit}`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch activity");
  return res.json();
}

export async function getRiskDistribution(): Promise<RiskDistribution> {
  const res = await fetch(`${API_BASE}/api/v1/dashboard/risk-distribution`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch risk distribution");
  return res.json();
}

export async function getHighRiskCase(): Promise<any> {
  const res = await fetch(`${API_BASE}/api/v1/dashboard/high-risk-case`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch high-risk case");
  return res.json();
}
