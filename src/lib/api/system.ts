const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface SystemHealth {
  status: string;
  backend: { status: string };
  engines: Record<string, string>;
  database: { status: string };
  timestamp: string;
}

export interface EngineInfo {
  id: string;
  name: string;
  status: string;
  model: string;
  version: string;
  last_loaded: string | null;
}

export async function getSystemHealth(): Promise<SystemHealth> {
  const res = await fetch(`${API_BASE}/api/v1/system/health`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch system health");
  return res.json();
}

export async function getSystemEngines(): Promise<{ engines: EngineInfo[] }> {
  const res = await fetch(`${API_BASE}/api/v1/system/engines`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error("Failed to fetch system engines");
  return res.json();
}
