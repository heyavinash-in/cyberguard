"use client"

import { useState } from "react"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { RiskIndicator } from "@/components/ui/risk-indicator"
import { Input } from "@/components/ui/input"
import {
  ShieldAlert,
  Loader2,
  User,
  Monitor,
  MapPin,
  Clock,
  Key,
  ShieldCheck,
  Activity,
  History,
  AlertTriangle,
  Lock,
  Globe,
  Wifi,
  Smartphone
} from "lucide-react"

import { AccountActivityRequest, AccountActivityResponse, analyzeAccountActivity } from "@/lib/account-security-api"

export default function AccountSecurityPage() {
  const [formData, setFormData] = useState<AccountActivityRequest>({
    user_id: "user_001",
    timestamp: new Date().toISOString(),
    ip_address: "",
    country: "",
    city: "",
    device_id: "",
    device_type: "Windows",
    login_success: true,
    failed_login_count: 0,
    mfa_used: true,
    mfa_configuration_changed: false,
    session_id: "sess_" + Math.floor(Math.random() * 1000),
    active_session_count: 1,
    vpn_detected: false,
    event_description: ""
  })
  
  const [status, setStatus] = useState<"idle" | "analyzing" | "complete">("idle")
  const [result, setResult] = useState<AccountActivityResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleInputChange = (field: keyof AccountActivityRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const simulateNormal = () => {
    setFormData({
      user_id: "user_001",
      timestamp: new Date().toISOString(),
      ip_address: "203.0.113.10",
      country: "India",
      city: "Bhubaneswar",
      device_id: "device_windows_01",
      device_type: "Windows",
      login_success: true,
      failed_login_count: 0,
      mfa_used: true,
      mfa_configuration_changed: false,
      session_id: "sess_" + Math.floor(Math.random() * 1000),
      active_session_count: 1,
      vpn_detected: false,
      event_description: "Standard morning login"
    })
  }

  const simulateTakeover = () => {
    setFormData({
      user_id: "user_001",
      timestamp: new Date(Date.now() - 3600000 * 5).toISOString(), // 5 hours ago (unusual time simulated if outside 8-19)
      ip_address: "198.51.100.42",
      country: "Singapore",
      city: "Singapore",
      device_id: "device_unknown_mac",
      device_type: "macOS",
      login_success: true,
      failed_login_count: 7,
      mfa_used: true,
      mfa_configuration_changed: true,
      session_id: "sess_" + Math.floor(Math.random() * 1000),
      active_session_count: 3,
      vpn_detected: true,
      event_description: "Multiple failed attempts followed by MFA hijack"
    })
  }

  const handleAnalyze = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    
    // Basic frontend validation
    if (!formData.user_id || !formData.ip_address || !formData.country || !formData.device_id) {
      setError("Please fill all required fields (User ID, IP, Country, Device ID).")
      return
    }

    setStatus("analyzing")
    setError(null)
    setResult(null)

    try {
      const response = await analyzeAccountActivity(formData)
      setResult(response)
      setStatus("complete")
    } catch (err: any) {
      setError(err.message || "An error occurred during analysis")
      setStatus("idle")
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Account Takeover Analyzer</h1>
        <p className="text-muted-foreground">
          Analyze account activity against an established behavioral baseline.
        </p>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {status === "idle" && (
        <div className="grid lg:grid-cols-2 gap-6">
          <Card className="border-primary/20 bg-card">
            <CardHeader>
              <CardTitle>Analyze Account Activity</CardTitle>
              <CardDescription>Enter telemetry data to evaluate behavioral deviation.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAnalyze} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-muted-foreground">User ID *</label>
                    <Input value={formData.user_id} onChange={(e) => handleInputChange("user_id", e.target.value)} placeholder="user_001" required />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-muted-foreground">IP Address *</label>
                    <Input value={formData.ip_address} onChange={(e) => handleInputChange("ip_address", e.target.value)} placeholder="203.0.113.10" required />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-muted-foreground">Country *</label>
                    <Input value={formData.country} onChange={(e) => handleInputChange("country", e.target.value)} placeholder="India" required />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-muted-foreground">Device ID *</label>
                    <Input value={formData.device_id} onChange={(e) => handleInputChange("device_id", e.target.value)} placeholder="device_windows_01" required />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2 flex flex-col">
                    <label className="text-xs font-semibold text-muted-foreground mb-2">Device Type</label>
                    <select 
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                      value={formData.device_type} 
                      onChange={(e) => handleInputChange("device_type", e.target.value)}
                    >
                      <option value="Windows">Windows</option>
                      <option value="macOS">macOS</option>
                      <option value="Linux">Linux</option>
                      <option value="Android">Android</option>
                      <option value="iOS">iOS</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-muted-foreground">Failed Login Count</label>
                    <Input type="number" min="0" value={formData.failed_login_count} onChange={(e) => handleInputChange("failed_login_count", parseInt(e.target.value) || 0)} />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2 flex flex-col">
                    <label className="text-xs font-semibold text-muted-foreground mb-2">Login Success</label>
                    <select 
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                      value={formData.login_success ? "true" : "false"} 
                      onChange={(e) => handleInputChange("login_success", e.target.value === "true")}
                    >
                      <option value="true">Successful</option>
                      <option value="false">Failed</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-muted-foreground">Active Sessions</label>
                    <Input type="number" min="0" value={formData.active_session_count} onChange={(e) => handleInputChange("active_session_count", parseInt(e.target.value) || 0)} />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mt-2">
                  <label className="flex items-center space-x-2 text-sm text-muted-foreground cursor-pointer">
                    <input type="checkbox" checked={formData.mfa_configuration_changed} onChange={(e) => handleInputChange("mfa_configuration_changed", e.target.checked)} className="rounded border-gray-300 text-primary focus:ring-primary" />
                    <span>MFA Config Changed</span>
                  </label>
                  <label className="flex items-center space-x-2 text-sm text-muted-foreground cursor-pointer">
                    <input type="checkbox" checked={formData.vpn_detected} onChange={(e) => handleInputChange("vpn_detected", e.target.checked)} className="rounded border-gray-300 text-primary focus:ring-primary" />
                    <span>VPN Detected</span>
                  </label>
                </div>

                <div className="pt-4 flex flex-col sm:flex-row gap-3">
                  <Button type="submit" className="w-full sm:w-auto"><Activity className="mr-2 h-4 w-4" /> Analyze Activity</Button>
                </div>
              </form>
            </CardContent>
          </Card>

          <div className="space-y-6">
            <Card className="border-emerald-500/20 bg-emerald-500/5">
              <CardHeader>
                <CardTitle className="text-emerald-500">Normal Activity</CardTitle>
                <CardDescription>Simulate standard behavior for this baseline.</CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full border-emerald-500/30 hover:bg-emerald-500/10 text-emerald-500" onClick={simulateNormal}>
                  <ShieldCheck className="mr-2 h-4 w-4" /> Simulate Normal Activity
                </Button>
              </CardContent>
            </Card>

            <Card className="border-destructive/20 bg-destructive/5">
              <CardHeader>
                <CardTitle className="text-destructive">Account Takeover</CardTitle>
                <CardDescription>Simulate a realistic synthetic attack sequence.</CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full border-destructive/30 hover:bg-destructive/10 text-destructive" onClick={simulateTakeover}>
                  <ShieldAlert className="mr-2 h-4 w-4" /> Simulate Account Takeover
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {status === "analyzing" && (
        <Card className="border-primary/20 bg-primary/5">
          <CardContent className="pt-6 flex flex-col items-center justify-center min-h-[300px] space-y-4">
            <Loader2 className="h-12 w-12 animate-spin text-primary" />
            <h3 className="text-xl font-semibold">Running Behavioral Analysis...</h3>
            <p className="text-muted-foreground text-sm max-w-md text-center">
              Extracting features, evaluating deterministic rules, and executing Isolation Forest anomaly detection against the established baseline.
            </p>
          </CardContent>
        </Card>
      )}

      {status === "complete" && result && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Analysis Result</h2>
            <Button variant="outline" onClick={() => setStatus("idle")}>New Analysis</Button>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <Card className={`border-${result.risk_level === 'CRITICAL' ? 'red' : result.risk_level === 'HIGH' ? 'orange' : result.risk_level === 'MEDIUM' ? 'yellow' : result.risk_level === 'LOW' ? 'blue' : 'emerald'}-500/30`}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-2xl flex items-center gap-2 mb-1">
                        {result.risk_level === 'CRITICAL' || result.risk_level === 'HIGH' ? <ShieldAlert className="h-6 w-6 text-destructive" /> : <ShieldCheck className="h-6 w-6 text-emerald-500" />}
                        {result.classification.replace(/_/g, ' ')}
                      </CardTitle>
                      <CardDescription className="text-base text-foreground/80">{result.explanation}</CardDescription>
                    </div>
                    <div className="text-right">
                      <span className={`text-4xl font-bold ${
                        result.risk_level === 'CRITICAL' ? 'text-red-500' :
                        result.risk_level === 'HIGH' ? 'text-orange-500' :
                        result.risk_level === 'MEDIUM' ? 'text-yellow-500' :
                        result.risk_level === 'LOW' ? 'text-blue-500' : 'text-emerald-500'
                      }`}>
                        {result.risk_score}
                      </span>
                      <span className="text-muted-foreground text-sm block">/ 100</span>
                    </div>
                  </div>
                </CardHeader>
              </Card>

              {result.correlations.length > 0 && (
                <Card className="border-amber-500/30 bg-amber-500/5">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-amber-500 text-sm tracking-wider uppercase">Detected Attack Patterns</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {result.correlations.map((corr, idx) => (
                      <div key={idx} className="flex gap-3">
                        <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0" />
                        <div>
                          <strong className="block text-foreground">{corr.type.replace(/_/g, ' ')}</strong>
                          <p className="text-sm text-muted-foreground mt-0.5">{corr.description}</p>
                        </div>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Behavioral Baseline Comparison</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="p-3 bg-muted/40 rounded-lg border border-border">
                      <MapPin className="h-5 w-5 mb-2 text-muted-foreground" />
                      <div className="text-sm text-muted-foreground mb-1">Country</div>
                      <div className={`font-semibold ${result.baseline_comparison.country === 'NEW' ? 'text-amber-500' : 'text-emerald-500'}`}>
                        {result.baseline_comparison.country}
                      </div>
                    </div>
                    <div className="p-3 bg-muted/40 rounded-lg border border-border">
                      <Monitor className="h-5 w-5 mb-2 text-muted-foreground" />
                      <div className="text-sm text-muted-foreground mb-1">Device</div>
                      <div className={`font-semibold ${result.baseline_comparison.device === 'NEW' ? 'text-amber-500' : 'text-emerald-500'}`}>
                        {result.baseline_comparison.device}
                      </div>
                    </div>
                    <div className="p-3 bg-muted/40 rounded-lg border border-border">
                      <Globe className="h-5 w-5 mb-2 text-muted-foreground" />
                      <div className="text-sm text-muted-foreground mb-1">IP Address</div>
                      <div className={`font-semibold ${result.baseline_comparison.ip === 'NEW' ? 'text-amber-500' : 'text-emerald-500'}`}>
                        {result.baseline_comparison.ip}
                      </div>
                    </div>
                    <div className="p-3 bg-muted/40 rounded-lg border border-border">
                      <Clock className="h-5 w-5 mb-2 text-muted-foreground" />
                      <div className="text-sm text-muted-foreground mb-1">Login Time</div>
                      <div className={`font-semibold ${result.baseline_comparison.login_hour === 'UNUSUAL' ? 'text-amber-500' : 'text-emerald-500'}`}>
                        {result.baseline_comparison.login_hour}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Evidence & Anomalies</CardTitle>
                </CardHeader>
                <CardContent>
                  {result.findings.length === 0 ? (
                    <p className="text-sm text-muted-foreground flex items-center gap-2">
                      <ShieldCheck className="h-4 w-4 text-emerald-500" /> No behavioral anomalies detected.
                    </p>
                  ) : (
                    <ul className="space-y-4">
                      {result.findings.map((f, idx) => (
                        <li key={idx} className="flex gap-4 p-4 bg-muted/20 rounded-lg border border-border/50">
                          <div className={`mt-0.5 w-2 h-2 rounded-full shrink-0 ${f.severity === 'HIGH' ? 'bg-destructive' : f.severity === 'MEDIUM' ? 'bg-amber-500' : 'bg-blue-500'}`} />
                          <div className="flex-1">
                            <strong className="block mb-1">{f.title}</strong>
                            <p className="text-sm text-muted-foreground">{f.explanation}</p>
                            <p className="text-xs text-muted-foreground/60 mt-2 font-mono">{f.evidence}</p>
                          </div>
                          <div className="text-right">
                            <span className="text-xs font-semibold text-muted-foreground block mb-1">Impact</span>
                            <span className="text-sm font-bold">+{f.contribution} pts</span>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Recommended Response</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {result.recommended_actions.map((act, i) => (
                    <Button key={i} variant={i === 0 && result.risk_level === 'CRITICAL' ? "destructive" : "secondary"} className="w-full justify-start text-left h-auto py-3">
                      <Lock className="mr-2 h-4 w-4 shrink-0" /> {act}
                    </Button>
                  ))}
                  <p className="text-[10px] text-center text-muted-foreground mt-4 italic">* Prototype simulated actions</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Incident Timeline</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="relative border-l border-border ml-3 space-y-6">
                    {result.timeline.map((event, i) => (
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

              <Card className="bg-muted/30">
                <CardHeader className="pb-3">
                  <CardTitle className="text-xs uppercase tracking-wider text-muted-foreground">Engine Metadata</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Anomaly ML</span>
                    <span className="font-mono">{result.model_info.anomaly_detector}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Rule Engine</span>
                    <span className="font-mono">{result.model_info.rule_engine_version}</span>
                  </div>
                  <div className="flex justify-between mt-2 pt-2 border-t border-border/50">
                    <span className="text-muted-foreground">Latency</span>
                    <span className="font-mono text-emerald-400">{result.processing.latency_ms}ms</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
