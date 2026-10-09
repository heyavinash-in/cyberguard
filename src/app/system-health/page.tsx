"use client"

import { useEffect, useState } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { ActivitySquare, Database, Server, Cpu, CheckCircle2, XCircle, AlertCircle } from "lucide-react"

import { getSystemHealth, SystemHealth } from "@/lib/api/system"

export default function SystemHealthPage() {
  const [health, setHealth] = useState<SystemHealth | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchHealth = async () => {
    try {
      const res = await getSystemHealth()
      setHealth(res)
      setError(null)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHealth()
    const interval = setInterval(fetchHealth, 10000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <ActivitySquare className="h-12 w-12 animate-spin text-primary mb-4" />
        <h2 className="text-xl font-bold">Loading System Health...</h2>
      </div>
    )
  }

  const getStatusIcon = (status: string) => {
    if (status === "operational") return <CheckCircle2 className="h-5 w-5 text-emerald-500" />
    if (status === "not_configured") return <AlertCircle className="h-5 w-5 text-amber-500" />
    return <XCircle className="h-5 w-5 text-destructive" />
  }

  const overallStatus = error ? "offline" : health?.status || "offline"

  return (
    <div className="max-w-[1200px] mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 border-b border-border/50 pb-6">
        <div>
          <h1 className="text-4xl font-black tracking-tight mb-2 bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">SYSTEM HEALTH</h1>
          <p className="text-muted-foreground text-lg">Real-time status of CyberGuard infrastructure and engines.</p>
        </div>
        <div className="flex items-center gap-2 font-mono text-sm">
          Last checked: {new Date().toLocaleTimeString()}
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className={`border-border/50 bg-card/40 backdrop-blur-sm ${overallStatus === 'operational' ? 'border-t-4 border-t-emerald-500' : 'border-t-4 border-t-destructive'}`}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Server className="h-5 w-5" /> Overall Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <span className="font-semibold uppercase tracking-wider text-muted-foreground">Platform</span>
              <div className="flex items-center gap-2">
                {getStatusIcon(overallStatus)}
                <span className={`font-bold uppercase ${overallStatus === 'operational' ? 'text-emerald-500' : 'text-destructive'}`}>
                  {overallStatus}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50 bg-card/40 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" /> Infrastructure
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center border-b border-border/50 pb-2">
              <span className="text-muted-foreground">Backend API</span>
              <div className="flex items-center gap-2">
                {getStatusIcon(health?.backend?.status || "offline")}
                <span className="text-sm font-semibold uppercase">{health?.backend?.status || "offline"}</span>
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground">Database (SQLite)</span>
              <div className="flex items-center gap-2">
                {getStatusIcon(health?.database?.status || "offline")}
                <span className="text-sm font-semibold uppercase">{health?.database?.status || "offline"}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50 bg-card/40 backdrop-blur-sm lg:col-span-1 md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Cpu className="h-5 w-5" /> Detection Engines
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {health?.engines && Object.entries(health.engines).map(([name, status]) => (
              <div key={name} className="flex justify-between items-center border-b border-border/50 pb-2 last:border-0 last:pb-0">
                <span className="text-muted-foreground uppercase">{name}</span>
                <div className="flex items-center gap-2">
                  {getStatusIcon(status)}
                  <span className={`text-sm font-semibold uppercase ${status === 'not_configured' ? 'text-amber-500' : status === 'operational' ? 'text-emerald-500' : 'text-destructive'}`}>
                    {status.replace("_", " ")}
                  </span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
