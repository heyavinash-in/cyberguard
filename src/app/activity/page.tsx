"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Activity, Clock } from "lucide-react"

import { getDashboardActivity, DashboardActivity } from "@/lib/api/dashboard"

export default function ActivityTimelinePage() {
  const router = useRouter()
  const [activity, setActivity] = useState<DashboardActivity[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const res = await getDashboardActivity(50)
        setActivity(res.items)
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
        <h2 className="text-xl font-bold">Loading Timeline...</h2>
      </div>
    )
  }

  return (
    <div className="max-w-[1200px] mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 border-b border-border/50 pb-6">
        <div>
          <h1 className="text-4xl font-black tracking-tight mb-2 bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">ACTIVITY TIMELINE</h1>
          <p className="text-muted-foreground text-lg">Real-time log of all analysis events across all engines.</p>
        </div>
      </div>

      <Card className="border-border/50 bg-card/40 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5 text-primary" />
            Recent Events
          </CardTitle>
        </CardHeader>
        <CardContent>
          {activity.length === 0 ? (
            <div className="text-center p-12 text-muted-foreground border border-dashed border-border/50 rounded-lg bg-background/50">
              <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No activity recorded yet.</p>
            </div>
          ) : (
            <div className="relative border-l-2 border-border/50 ml-3 md:ml-6 space-y-8 py-4">
              {activity.map((item) => {
                const isCrit = item.risk_level === "CRITICAL"
                const isHigh = item.risk_level === "HIGH"
                const isMed = item.risk_level === "MEDIUM"
                
                const dotColor = isCrit ? 'bg-destructive' : isHigh ? 'bg-orange-500' : isMed ? 'bg-amber-500' : 'bg-emerald-500'
                const bgColor = isCrit ? 'bg-destructive/10 border-destructive/30' : isHigh ? 'bg-orange-500/10 border-orange-500/30' : 'bg-muted/20 border-border/50'

                return (
                  <div key={item.id} className="relative pl-6 md:pl-8 pr-4 cursor-pointer hover:opacity-80 transition-opacity" onClick={() => router.push('/threat-cases')}>
                    <div className={`absolute -left-[9px] top-1.5 w-4 h-4 rounded-full ${dotColor} ring-4 ring-background`} />
                    
                    <div className={`p-4 rounded-lg border ${bgColor}`}>
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
                        <div>
                          <div className="text-xs font-mono text-muted-foreground mb-1">
                            {new Date(item.timestamp).toLocaleString()}
                          </div>
                          <h4 className="font-semibold text-lg">{item.title}</h4>
                          <div className="flex flex-wrap items-center gap-3 mt-2">
                            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                              {item.engine} ENGINE
                            </span>
                            <span className="text-xs text-muted-foreground">•</span>
                            <span className="text-xs font-medium">{item.classification.replace(/_/g, " ")}</span>
                          </div>
                        </div>
                        
                        <div className="flex items-center gap-4 shrink-0">
                          <div className={`px-2 py-1 rounded text-xs font-bold ${isCrit ? 'bg-destructive/20 text-destructive' : isHigh ? 'bg-orange-500/20 text-orange-500' : isMed ? 'bg-amber-500/20 text-amber-500' : 'bg-emerald-500/20 text-emerald-500'}`}>
                            {item.risk_level}
                          </div>
                          <div className="text-xl font-bold font-mono w-12 text-right">
                            {item.risk_score}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
