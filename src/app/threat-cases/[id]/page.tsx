"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Activity, ShieldAlert, AlertTriangle, Shield, Clock } from "lucide-react"

import { getCase, ThreatCaseDetail } from "@/lib/api/cases"

export default function ThreatCaseDetailPage() {
  const params = useParams()
  const router = useRouter()
  const caseId = params.id as string

  const [caseData, setCaseData] = useState<ThreatCaseDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await getCase(caseId)
        setCaseData(res)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    if (caseId) load()
  }, [caseId])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <Activity className="h-12 w-12 animate-spin text-primary mb-4" />
        <h2 className="text-xl font-bold">Loading Case Details...</h2>
      </div>
    )
  }

  if (error || !caseData) {
    return (
      <div className="p-8 text-center text-destructive">
        <h2 className="text-xl font-bold mb-2">Error Loading Case</h2>
        <p>{error || "Case not found"}</p>
        <Button variant="outline" className="mt-4" onClick={() => router.push('/threat-cases')}>
          Return to Cases
        </Button>
      </div>
    )
  }

  const raw = caseData.raw_result
  const findings = raw.findings || []
  const recommendedActions = raw.recommended_actions || raw.recommended_response || []
  const timeline = raw.timeline || []

  return (
    <div className="max-w-[1200px] mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      <div>
        <Button variant="ghost" onClick={() => router.push('/threat-cases')} className="mb-4 pl-0 hover:bg-transparent text-muted-foreground hover:text-foreground">
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Cases
        </Button>
        <h1 className="text-3xl font-black tracking-tight mb-2 uppercase flex items-center gap-3">
          <ShieldAlert className="h-8 w-8 text-destructive" />
          {caseData.id}
        </h1>
        <p className="text-muted-foreground">Opened: {new Date(caseData.timestamp).toLocaleString()}</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        
        <div className="lg:col-span-1 space-y-6">
          <Card className="border-border/50 bg-card/40 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">Case Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between border-b border-border/50 pb-2">
                <span className="text-muted-foreground text-sm">Status</span>
                <span className="font-semibold text-sm px-2 py-0.5 rounded bg-blue-500/20 text-blue-400">{caseData.status}</span>
              </div>
              <div className="flex justify-between border-b border-border/50 pb-2">
                <span className="text-muted-foreground text-sm">Engine</span>
                <span className="font-semibold text-sm uppercase">{caseData.engine}</span>
              </div>
              <div className="flex justify-between border-b border-border/50 pb-2">
                <span className="text-muted-foreground text-sm">Classification</span>
                <span className="font-semibold text-sm">{caseData.classification}</span>
              </div>
              <div className="flex justify-between border-b border-border/50 pb-2">
                <span className="text-muted-foreground text-sm">Risk Level</span>
                <span className="font-bold text-sm text-destructive">{caseData.risk_level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground text-sm">Risk Score</span>
                <span className="font-mono text-lg font-bold">{caseData.risk_score}</span>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-border/50 bg-card/40 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                <Shield className="h-4 w-4" /> Recommended Response
              </CardTitle>
            </CardHeader>
            <CardContent>
              {recommendedActions.length > 0 ? (
                <ul className="space-y-2">
                  {recommendedActions.map((act: string, i: number) => (
                    <li key={i} className="text-sm flex gap-2 p-2 bg-muted/30 rounded border border-border/50">
                      <div className="text-primary">•</div> {act}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">No specific actions recommended.</p>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <Card className="border-destructive/20 bg-destructive/5 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-destructive">
                <AlertTriangle className="h-5 w-5" /> EXPLANATION
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg font-medium">{caseData.summary}</p>
            </CardContent>
          </Card>

          <Card className="border-border/50 bg-card/40 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">EVIDENCE</CardTitle>
            </CardHeader>
            <CardContent>
              {findings.length > 0 ? (
                <ul className="space-y-3">
                  {findings.map((f: any, i: number) => (
                    <li key={i} className="p-3 bg-muted/20 rounded-lg border border-border/50">
                      <div className="font-medium text-sm">{typeof f === 'string' ? f : f.title}</div>
                      {f.explanation && <div className="text-xs text-muted-foreground mt-1">{f.explanation}</div>}
                      {f.evidence && <div className="text-xs font-mono text-muted-foreground/60 mt-1.5">{f.evidence}</div>}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">No detailed findings available.</p>
              )}
            </CardContent>
          </Card>

          {timeline.length > 0 && (
            <Card className="border-border/50 bg-card/40 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                  <Clock className="h-4 w-4" /> TIMELINE
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="relative border-l border-border ml-3 space-y-6">
                  {timeline.map((event: any, i: number) => (
                    <div key={i} className="relative pl-6">
                      <div className="absolute -left-1.5 top-1.5 w-3 h-3 rounded-full bg-primary ring-4 ring-background" />
                      <div className="text-xs text-muted-foreground mb-1">{new Date(event.timestamp).toLocaleTimeString()}</div>
                      <div className="font-semibold text-sm">{event.event}</div>
                      <div className="text-sm text-muted-foreground mt-1">{event.description}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
        
      </div>
    </div>
  )
}
