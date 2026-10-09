"use client"

import { useState } from "react"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { RiskIndicator } from "@/components/ui/risk-indicator"
import { 
  ShieldAlert, 
  AlertTriangle, 
  Search, 
  Globe, 
  Mail, 
  FileImage,
  ChevronRight,
  ShieldCheck,
  Server,
  Lock,
  ArrowUpRight
} from "lucide-react"

type Threat = {
  id: string
  target: string
  type: string
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
  score: number
  date: string
  sourceIp: string
  status: "Active" | "Mitigated"
  description: string
}

const THREATS_DATA: Threat[] = [
  {
    id: "TR-9921",
    target: "paypal-verify-auth.com",
    type: "Phishing URL",
    severity: "CRITICAL",
    score: 94,
    date: "2026-09-04 10:15:00",
    sourceIp: "192.0.2.144",
    status: "Active",
    description: "URL mimics financial institution. Credential harvesting detected."
  },
  {
    id: "TR-9920",
    target: "invoice_77812.pdf.exe",
    type: "Malicious File",
    severity: "HIGH",
    score: 88,
    date: "2026-09-04 09:40:00",
    sourceIp: "198.51.100.22",
    status: "Active",
    description: "Double extension payload attempting to drop a reverse shell."
  },
  {
    id: "TR-9919",
    target: "Suspicious Login",
    type: "Account Hijack",
    severity: "HIGH",
    score: 75,
    date: "2026-09-04 08:30:00",
    sourceIp: "203.0.113.1",
    status: "Mitigated",
    description: "Impossible travel alert triggered for admin account."
  },
  {
    id: "TR-9918",
    target: "Suspicious SMS",
    type: "Smishing",
    severity: "MEDIUM",
    score: 55,
    date: "2026-09-03 18:20:00",
    sourceIp: "N/A",
    status: "Mitigated",
    description: "Text message requesting urgent package delivery fee."
  }
]

export default function ThreatsPage() {
  const [filter, setFilter] = useState("ALL")
  const [selectedThreatId, setSelectedThreatId] = useState<string | null>(THREATS_DATA[0].id)

  const filteredThreats = THREATS_DATA.filter(t => filter === "ALL" || t.severity === filter)
  const selectedThreat = THREATS_DATA.find(t => t.id === selectedThreatId)

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-4">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Threat Intelligence</h1>
        <p className="text-muted-foreground">Detailed logs of detected anomalies and security risks.</p>
      </div>

      <div className="flex-1 flex flex-col md:flex-row gap-6 overflow-hidden pt-2">
        {/* Left Pane: Threat List */}
        <Card className="w-full md:w-1/3 lg:w-[400px] flex flex-col overflow-hidden bg-card border-primary/10">
          <CardHeader className="px-4 py-3 border-b pb-4">
            <div className="flex items-center justify-between mb-3">
              <CardTitle className="text-lg">Detections</CardTitle>
              <Badge variant="outline">{filteredThreats.length} items</Badge>
            </div>
            <div className="flex flex-wrap gap-2">
              {["ALL", "CRITICAL", "HIGH", "MEDIUM"].map(f => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-3 py-1 text-xs font-semibold rounded-full border transition-colors ${
                    filter === f 
                    ? "bg-primary text-primary-foreground border-primary" 
                    : "bg-background text-muted-foreground hover:bg-accent border-border"
                  }`}
                >
                  {f}
                </button>
              ))}
            </div>
          </CardHeader>
          <div className="flex-1 overflow-y-auto">
            {filteredThreats.map((threat) => (
              <button
                key={threat.id}
                onClick={() => setSelectedThreatId(threat.id)}
                className={`w-full text-left p-4 border-b last:border-b-0 transition-colors flex items-center justify-between group ${
                  selectedThreatId === threat.id ? "bg-accent/80 border-l-4 border-l-primary" : "hover:bg-accent/40 border-l-4 border-l-transparent"
                }`}
              >
                <div className="truncate pr-4">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`h-2 w-2 rounded-full ${threat.severity === 'CRITICAL' ? 'bg-red-500' : threat.severity === 'HIGH' ? 'bg-orange-500' : 'bg-yellow-500'}`} />
                    <span className="font-semibold text-sm truncate">{threat.target}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{threat.id}</span>
                    <span>•</span>
                    <span className="truncate">{threat.type}</span>
                  </div>
                </div>
                <ChevronRight className={`h-4 w-4 shrink-0 transition-transform ${selectedThreatId === threat.id ? 'text-primary translate-x-1' : 'text-muted-foreground group-hover:translate-x-1'}`} />
              </button>
            ))}
            {filteredThreats.length === 0 && (
              <div className="p-8 text-center text-muted-foreground text-sm">
                No threats match the current filter.
              </div>
            )}
          </div>
        </Card>

        {/* Right Pane: Investigation Details */}
        <Card className="flex-1 flex flex-col overflow-hidden bg-card border-primary/20">
          {selectedThreat ? (
            <>
              <CardHeader className="border-b bg-muted/20 px-6 py-5">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <Badge variant={selectedThreat.severity === "CRITICAL" ? "destructive" : "warning"}>
                        {selectedThreat.severity} THREAT
                      </Badge>
                      <Badge variant={selectedThreat.status === "Active" ? "destructive" : "success"} className={selectedThreat.status === "Active" ? "bg-red-500/10 text-red-500 border-red-500/20" : ""}>
                        {selectedThreat.status}
                      </Badge>
                    </div>
                    <CardTitle className="text-2xl">{selectedThreat.target}</CardTitle>
                    <CardDescription className="mt-1 flex items-center gap-4 text-sm">
                      <span>ID: {selectedThreat.id}</span>
                      <span>{selectedThreat.date}</span>
                    </CardDescription>
                  </div>
                  <Button variant="outline" size="sm" className="hidden sm:flex">
                    <ArrowUpRight className="mr-2 h-4 w-4" /> Export Report
                  </Button>
                </div>
              </CardHeader>
              
              <div className="flex-1 overflow-y-auto p-6 space-y-8">
                <div className="grid md:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <div>
                      <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground border-b pb-2 mb-4">Risk Assessment</h4>
                      <RiskIndicator score={selectedThreat.score} />
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground border-b pb-2 mb-4">Threat Synopsis</h4>
                      <p className="text-sm leading-relaxed">{selectedThreat.description}</p>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground border-b pb-2">Telemetry Data</h4>
                    <div className="bg-secondary/50 rounded-lg p-4 space-y-3 border">
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Threat Type</span>
                        <span className="font-medium">{selectedThreat.type}</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Source IP</span>
                        <span className="font-medium font-mono">{selectedThreat.sourceIp}</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Action Taken</span>
                        <span className={selectedThreat.status === "Active" ? "text-destructive font-medium" : "text-emerald-500 font-medium"}>
                          {selectedThreat.status === "Active" ? "Pending Admin Review" : "Automatically Blocked"}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {selectedThreat.status === "Active" && (
                  <div className="flex gap-4 pt-4 border-t">
                    <Button variant="destructive" className="flex-1">Isolate / Block Source</Button>
                    <Button variant="outline" className="flex-1">Mark as False Positive</Button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground p-8 text-center">
              <ShieldCheck className="h-16 w-16 mb-4 opacity-20" />
              <p className="text-lg font-semibold text-foreground">Select a Threat</p>
              <p className="max-w-xs">Click on an item in the detection list to view the full investigation telemetry.</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}
