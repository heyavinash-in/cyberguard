"use client"

import { useEffect, useState } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Server, Activity, CheckCircle2, AlertCircle } from "lucide-react"

import { getSystemEngines, EngineInfo } from "@/lib/api/system"

export default function ModelsPage() {
  const [engines, setEngines] = useState<EngineInfo[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const res = await getSystemEngines()
        setEngines(res.engines)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <Activity className="h-12 w-12 animate-spin text-primary mb-4" />
        <h2 className="text-xl font-bold">Loading Models & Engines...</h2>
      </div>
    )
  }

  return (
    <div className="max-w-[1200px] mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 border-b border-border/50 pb-6">
        <div>
          <h1 className="text-4xl font-black tracking-tight mb-2 bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">MODELS & ENGINES</h1>
          <p className="text-muted-foreground text-lg">Active AI models and detection pipelines powering CyberGuard.</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {engines.map((engine) => (
          <Card key={engine.id} className="border-border/50 bg-card/40 backdrop-blur-sm">
            <CardHeader className="border-b border-border/30 bg-muted/10">
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Server className="h-5 w-5 text-primary" />
                  {engine.name}
                </div>
                {engine.status === "operational" ? (
                  <div className="flex items-center gap-1 text-emerald-500 text-sm">
                    <CheckCircle2 className="h-4 w-4" /> Operational
                  </div>
                ) : (
                  <div className="flex items-center gap-1 text-amber-500 text-sm">
                    <AlertCircle className="h-4 w-4" /> Not Configured
                  </div>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6 space-y-4">
              <div className="grid grid-cols-3 gap-4 border-b border-border/50 pb-4">
                <div className="col-span-1 text-sm text-muted-foreground">Model Architecture</div>
                <div className="col-span-2 text-sm font-semibold">{engine.model}</div>
              </div>
              <div className="grid grid-cols-3 gap-4 border-b border-border/50 pb-4">
                <div className="col-span-1 text-sm text-muted-foreground">Version</div>
                <div className="col-span-2 text-sm font-mono">{engine.version}</div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div className="col-span-1 text-sm text-muted-foreground">Last Loaded</div>
                <div className="col-span-2 text-sm text-muted-foreground">
                  {engine.last_loaded ? new Date(engine.last_loaded).toLocaleString() : "N/A"}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
