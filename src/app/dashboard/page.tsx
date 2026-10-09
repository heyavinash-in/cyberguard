"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ShieldCheck, ShieldAlert, Activity, Search, AlertTriangle, LinkIcon, Mail, FileImage, Shield, Server, Clock } from "lucide-react"

import { 
  getDashboardSummary, getDashboardEngines, getDashboardActivity, getRiskDistribution, getHighRiskCase,
  DashboardSummary, EngineStats, DashboardActivity, RiskDistribution
} from "@/lib/api/dashboard"
import { getSystemHealth, SystemHealth } from "@/lib/api/system"

export default function DashboardPage() {
  const router = useRouter()
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [engines, setEngines] = useState<EngineStats[]>([])
  const [activity, setActivity] = useState<DashboardActivity[]>([])
  const [riskDist, setRiskDist] = useState<RiskDistribution | null>(null)
  const [highRiskCase, setHighRiskCase] = useState<any | null>(null)
  const [health, setHealth] = useState<SystemHealth | null>(null)
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      const [sumRes, engRes, actRes, distRes, hrRes, healthRes] = await Promise.all([
        getDashboardSummary(),
        getDashboardEngines(),
        getDashboardActivity(5),
        getRiskDistribution(),
        getHighRiskCase(),
        getSystemHealth()
      ])
      
      setSummary(sumRes)
      setEngines(engRes.engines)
      setActivity(actRes.items)
      setRiskDist(distRes)
      setHighRiskCase(hrRes)
      setHealth(healthRes)
    } catch (err) {
      console.error("Dashboard fetch error", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <Activity className="h-12 w-12 animate-spin text-primary mb-4" />
        <h2 className="text-xl font-bold">Loading Command Center...</h2>
      </div>
    )
  }

  // Calculate system status
  let systemStatusText = "● ALL SYSTEMS OPERATIONAL"
  let systemStatusColor = "text-emerald-500"
  
  if (!health) {
    systemStatusText = "● BACKEND OFFLINE"
    systemStatusColor = "text-destructive"
  } else if (Object.values(health.engines).includes("not_configured")) {
    systemStatusText = "● PARTIAL SYSTEM AVAILABILITY"
    systemStatusColor = "text-amber-500"
  }

  return (
    <div className="max-w-[1600px] mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 border-b border-border/50 pb-6">
        <div>
          <h1 className="text-4xl font-black tracking-tight mb-2 bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">CYBERGUARD COMMAND CENTER</h1>
          <p className="text-muted-foreground text-lg">Real-time, Explainable AI for Zero-Day Threat Detection</p>
        </div>
        <div className={`font-mono font-semibold tracking-wide ${systemStatusColor} bg-background/50 backdrop-blur-sm px-4 py-2 rounded-lg border border-border`}>
          {systemStatusText}
        </div>
      </div>

      {/* METRICS ROW */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-primary/20 bg-background/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">Threats Detected</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-foreground">{summary?.threats_detected ?? 0}</div>
          </CardContent>
        </Card>
        <Card className="border-destructive/20 bg-destructive/5 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wider text-destructive">Critical Threats</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-destructive">{summary?.critical_threats ?? 0}</div>
          </CardContent>
        </Card>
        <Card className="border-primary/20 bg-background/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">Scans Analyzed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-foreground">{summary?.scans_analyzed ?? 0}</div>
          </CardContent>
        </Card>
        <Card className="border-primary/20 bg-background/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">Active Cases</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-blue-500">{summary?.active_cases ?? 0}</div>
          </CardContent>
        </Card>
      </div>

      {/* ENGINES ROW */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {engines.map(engine => {
          let icon = <Server className="h-5 w-5 text-muted-foreground" />
          if (engine.id === "url") icon = <LinkIcon className="h-5 w-5 text-blue-400" />
          if (engine.id === "message") icon = <Mail className="h-5 w-5 text-purple-400" />
          if (engine.id === "account") icon = <ShieldAlert className="h-5 w-5 text-amber-400" />
          if (engine.id === "media") icon = <FileImage className="h-5 w-5 text-emerald-400" />
          
          return (
            <Card key={engine.id} className="border-border/50 bg-card/40 backdrop-blur-sm hover:bg-card/60 transition-colors">
              <CardHeader className="pb-2 flex flex-row items-center gap-3 space-y-0">
                {icon}
                <CardTitle className="text-base uppercase tracking-wide">{engine.name}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 pt-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Status</span>
                  <span className={engine.status === "operational" ? "text-emerald-500 font-medium capitalize" : "text-amber-500 font-medium capitalize"}>
                    {engine.status.replace("_", " ")}
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Scans</span>
                  <span className="font-mono">{engine.total_scans}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Threats</span>
                  <span className="font-mono text-destructive">{engine.threats_detected}</span>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* LIVE ACTIVITY */}
        <Card className="lg:col-span-2 border-border/50 bg-card/40 backdrop-blur-sm flex flex-col h-full">
          <CardHeader className="border-b border-border/30">
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-primary" />
              LIVE THREAT ACTIVITY
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0 flex-1 overflow-hidden flex flex-col">
            {activity.length === 0 ? (
              <div className="p-8 text-center text-muted-foreground">
                <p>No threat activity recorded yet.</p>
                <p className="text-sm mt-2">Run an analysis to generate security events.</p>
              </div>
            ) : (
              <div className="divide-y divide-border/30 overflow-y-auto max-h-[400px]">
                {activity.map(item => {
                  const isHigh = item.risk_level === "HIGH" || item.risk_level === "CRITICAL"
                  const isMed = item.risk_level === "MEDIUM"
                  return (
                    <div 
                      key={item.id} 
                      className={`p-4 hover:bg-muted/20 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer border-l-2 ${isHigh ? 'border-l-destructive' : isMed ? 'border-l-amber-500' : 'border-l-emerald-500'}`}
                      onClick={() => router.push('/threat-cases')}
                    >
                      <div className="flex gap-4 items-start sm:items-center">
                        <div className="text-xs font-mono text-muted-foreground shrink-0 w-16">
                          {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                        <div>
                          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1 flex items-center gap-2">
                            {item.engine} ENGINE
                          </div>
                          <div className="font-medium text-foreground">{item.title}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4 shrink-0">
                        <div className={`px-2 py-1 rounded text-xs font-bold ${isHigh ? 'bg-destructive/20 text-destructive' : isMed ? 'bg-amber-500/20 text-amber-500' : 'bg-emerald-500/20 text-emerald-500'}`}>
                          {item.risk_level}
                        </div>
                        <div className="text-xl font-bold font-mono w-12 text-right">
                          {item.risk_score}
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* RISK DISTRIBUTION */}
        <Card className="border-border/50 bg-card/40 backdrop-blur-sm h-full flex flex-col">
          <CardHeader className="border-b border-border/30">
            <CardTitle>RISK DISTRIBUTION</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col justify-center pt-6">
            {!riskDist || (riskDist.safe === 0 && riskDist.low === 0 && riskDist.medium === 0 && riskDist.high === 0 && riskDist.critical === 0) ? (
              <div className="text-center text-muted-foreground py-10">No data available</div>
            ) : (
              <div className="space-y-4">
                {[
                  { label: "CRITICAL", value: riskDist.critical, color: "bg-red-500" },
                  { label: "HIGH", value: riskDist.high, color: "bg-orange-500" },
                  { label: "MEDIUM", value: riskDist.medium, color: "bg-amber-500" },
                  { label: "LOW", value: riskDist.low, color: "bg-blue-500" },
                  { label: "SAFE", value: riskDist.safe, color: "bg-emerald-500" },
                ].map(item => {
                  const total = riskDist.safe + riskDist.low + riskDist.medium + riskDist.high + riskDist.critical
                  const percent = total > 0 ? (item.value / total) * 100 : 0
                  return (
                    <div key={item.label} className="space-y-1">
                      <div className="flex justify-between text-xs font-semibold">
                        <span>{item.label}</span>
                        <span className="text-muted-foreground">{item.value}</span>
                      </div>
                      <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                        <div className={`h-full ${item.color}`} style={{ width: `${percent}%` }} />
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </CardContent>
        </Card>

      </div>

      {/* EXPLAINABLE THREAT ANALYSIS */}
      <Card className="border-border/50 bg-card/40 backdrop-blur-sm overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-destructive/5 to-transparent pointer-events-none" />
        <CardHeader className="border-b border-border/30 relative">
          <CardTitle className="text-xl">EXPLAINABLE THREAT ANALYSIS</CardTitle>
          <CardDescription>Most recent high-risk event</CardDescription>
        </CardHeader>
        <CardContent className="p-0 relative">
          {!highRiskCase || Object.keys(highRiskCase).length === 0 ? (
            <div className="p-10 text-center text-muted-foreground">
              <ShieldCheck className="h-12 w-12 text-emerald-500/50 mx-auto mb-4" />
              <p>No high-risk threats detected yet.</p>
            </div>
          ) : (
            <div className="grid lg:grid-cols-3 divide-y lg:divide-y-0 lg:divide-x divide-border/30">
              <div className="p-8 flex flex-col justify-center items-center text-center">
                <div className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
                  {highRiskCase.classification ? highRiskCase.classification.replace(/_/g, " ") : "THREAT DETECTED"}
                </div>
                <div className="text-7xl font-black text-destructive mb-2 font-mono">
                  {highRiskCase.risk_score || highRiskCase.risk?.score || 99}
                </div>
                <div className="text-sm font-bold bg-destructive/20 text-destructive px-3 py-1 rounded uppercase tracking-widest mb-4">
                  CRITICAL
                </div>
                <Button variant="outline" className="mt-4 w-full" onClick={() => router.push('/threat-cases')}>
                  Investigate Case <Search className="ml-2 h-4 w-4" />
                </Button>
              </div>
              
              <div className="p-8 lg:col-span-2 space-y-6">
                <div>
                  <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-3 flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                    Why CyberGuard flagged this:
                  </h4>
                  <ul className="space-y-2">
                    {(highRiskCase.findings || []).map((finding: any, i: number) => (
                      <li key={i} className="flex gap-3 text-sm">
                        <div className="mt-1.5 w-1.5 h-1.5 rounded-full bg-destructive shrink-0" />
                        <div>
                          <span className="font-medium text-foreground block">{typeof finding === 'string' ? finding : finding.title}</span>
                          {finding.explanation && <span className="text-muted-foreground text-xs block">{finding.explanation}</span>}
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-3 flex items-center gap-2">
                    <Shield className="h-4 w-4 text-primary" />
                    Recommended response:
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {(highRiskCase.recommended_actions || []).map((action: string, i: number) => (
                      <div key={i} className="bg-muted/30 border border-border/50 rounded p-3 text-sm flex gap-2">
                        <div className="text-primary mt-0.5">•</div>
                        {action}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
