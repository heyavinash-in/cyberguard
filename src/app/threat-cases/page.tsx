"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Search, ChevronRight, ShieldAlert, Activity } from "lucide-react"

import { getCases, ThreatCaseSummary } from "@/lib/api/cases"

export default function ThreatCasesPage() {
  const router = useRouter()
  const [cases, setCases] = useState<ThreatCaseSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const res = await getCases()
        setCases(res.items)
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
        <h2 className="text-xl font-bold">Loading Threat Cases...</h2>
      </div>
    )
  }

  return (
    <div className="max-w-[1600px] mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 border-b border-border/50 pb-6">
        <div>
          <h1 className="text-4xl font-black tracking-tight mb-2 bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">INVESTIGATION CASES</h1>
          <p className="text-muted-foreground text-lg">Manage and review high-risk threat detections.</p>
        </div>
      </div>

      <Card className="border-border/50 bg-card/40 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5 text-primary" />
            Active Cases
          </CardTitle>
        </CardHeader>
        <CardContent>
          {cases.length === 0 ? (
            <div className="text-center p-12 text-muted-foreground border border-dashed border-border/50 rounded-lg bg-background/50">
              <ShieldAlert className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No threat cases have been created yet.</p>
              <p className="text-sm mt-1">Cases are generated automatically from HIGH and CRITICAL risk detections.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-border/50 text-muted-foreground">
                    <th className="py-4 px-4 font-semibold uppercase tracking-wider text-xs">Case ID</th>
                    <th className="py-4 px-4 font-semibold uppercase tracking-wider text-xs">Time</th>
                    <th className="py-4 px-4 font-semibold uppercase tracking-wider text-xs">Engine</th>
                    <th className="py-4 px-4 font-semibold uppercase tracking-wider text-xs">Classification</th>
                    <th className="py-4 px-4 font-semibold uppercase tracking-wider text-xs">Risk</th>
                    <th className="py-4 px-4 font-semibold uppercase tracking-wider text-xs">Status</th>
                    <th className="py-4 px-4 font-semibold uppercase tracking-wider text-xs text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/30">
                  {cases.map((c) => {
                    const isCrit = c.risk_level === "CRITICAL"
                    const isHigh = c.risk_level === "HIGH"
                    
                    return (
                      <tr key={c.id} className="hover:bg-muted/30 transition-colors group">
                        <td className="py-4 px-4 font-mono font-medium">{c.id}</td>
                        <td className="py-4 px-4 text-muted-foreground font-mono text-xs">
                          {new Date(c.timestamp).toLocaleString()}
                        </td>
                        <td className="py-4 px-4">
                          <span className="px-2 py-1 rounded text-xs font-semibold uppercase tracking-wider bg-secondary/50 text-secondary-foreground border border-border">
                            {c.engine}
                          </span>
                        </td>
                        <td className="py-4 px-4 font-medium">{c.classification.replace(/_/g, " ")}</td>
                        <td className="py-4 px-4">
                          <div className="flex items-center gap-2">
                            <div className={`px-2 py-0.5 rounded text-[10px] font-bold ${isCrit ? 'bg-destructive/20 text-destructive' : isHigh ? 'bg-orange-500/20 text-orange-500' : 'bg-amber-500/20 text-amber-500'}`}>
                              {c.risk_level}
                            </div>
                            <span className="font-mono text-xs font-semibold">{c.risk_score}</span>
                          </div>
                        </td>
                        <td className="py-4 px-4">
                          <span className="px-2 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
                            {c.status}
                          </span>
                        </td>
                        <td className="py-4 px-4 text-right">
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="group-hover:bg-primary group-hover:text-primary-foreground transition-all"
                            onClick={() => router.push(`/threat-cases/${c.id}`)}
                          >
                            Investigate <ChevronRight className="ml-1 w-4 h-4" />
                          </Button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
