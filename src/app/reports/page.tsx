"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { RiskIndicator } from "@/components/ui/risk-indicator"
import { 
  Printer, 
  Download, 
  ShieldCheck, 
  FileText,
  Calendar,
  Clock,
  Target,
  Server,
  AlertTriangle
} from "lucide-react"

export default function ReportsPage() {
  const handlePrint = () => {
    window.print()
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 print:hidden">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Incident Report</h1>
          <p className="text-muted-foreground">Formal security assessment and remediation plan.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handlePrint}>
            <Printer className="mr-2 h-4 w-4" /> Print PDF
          </Button>
          <Button>
            <Download className="mr-2 h-4 w-4" /> Export JSON
          </Button>
        </div>
      </div>

      {/* Report Document Area - Designed to look good on screen and in print */}
      <Card className="bg-card border-border shadow-md print:shadow-none print:border-none print:bg-white print:text-black">
        <CardHeader className="border-b print:border-gray-300 pb-6">
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3">
              <ShieldCheck className="h-8 w-8 text-primary print:text-black" />
              <div>
                <CardTitle className="text-2xl">CyberGuard Security Intelligence</CardTitle>
                <p className="text-sm text-muted-foreground print:text-gray-600 mt-1">Automated Threat Assessment Report</p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-mono text-sm font-semibold">REF: CG-INC-9921</p>
              <p className="text-xs text-muted-foreground print:text-gray-600 mt-1">Generated: {new Date().toLocaleDateString()} {new Date().toLocaleTimeString()}</p>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="pt-8 space-y-10">
          
          {/* Executive Summary */}
          <section className="space-y-4">
            <h3 className="text-lg font-bold border-b pb-2 uppercase tracking-wide print:border-gray-300">Executive Summary</h3>
            <p className="text-sm leading-relaxed">
              On September 4, 2026, the CyberGuard system intercepted and analyzed a suspicious URL payload. The automated assessment engine classified the target as a <strong>High-Risk Phishing Operation</strong> actively attempting to harvest user credentials by impersonating a known financial institution. Immediate network blocking is recommended.
            </p>
          </section>

          {/* Target Fingerprint */}
          <section className="space-y-4">
            <h3 className="text-lg font-bold border-b pb-2 uppercase tracking-wide print:border-gray-300">Target Fingerprint</h3>
            <div className="grid sm:grid-cols-2 gap-4">
              <div className="bg-secondary/50 print:bg-gray-100 p-4 rounded-md">
                <div className="flex items-center gap-2 text-muted-foreground print:text-gray-600 mb-1">
                  <Target className="h-4 w-4" /> <span className="text-xs uppercase font-semibold">Primary Target</span>
                </div>
                <p className="font-mono text-sm break-all">https://paypal-verify-auth.com/login</p>
              </div>
              <div className="bg-secondary/50 print:bg-gray-100 p-4 rounded-md">
                <div className="flex items-center gap-2 text-muted-foreground print:text-gray-600 mb-1">
                  <Server className="h-4 w-4" /> <span className="text-xs uppercase font-semibold">Resolved IP</span>
                </div>
                <p className="font-mono text-sm">192.0.2.144 (AS: 44441)</p>
              </div>
              <div className="bg-secondary/50 print:bg-gray-100 p-4 rounded-md">
                <div className="flex items-center gap-2 text-muted-foreground print:text-gray-600 mb-1">
                  <Calendar className="h-4 w-4" /> <span className="text-xs uppercase font-semibold">Domain Age</span>
                </div>
                <p className="text-sm font-medium">12 Hours (Newly Registered)</p>
              </div>
              <div className="bg-secondary/50 print:bg-gray-100 p-4 rounded-md">
                <div className="flex items-center gap-2 text-muted-foreground print:text-gray-600 mb-1">
                  <FileText className="h-4 w-4" /> <span className="text-xs uppercase font-semibold">SSL Certificate</span>
                </div>
                <p className="text-sm font-medium">Let&apos;s Encrypt (DV)</p>
              </div>
            </div>
          </section>

          {/* Risk Assessment */}
          <section className="space-y-4">
            <h3 className="text-lg font-bold border-b pb-2 uppercase tracking-wide print:border-gray-300">Risk Assessment</h3>
            <div className="flex flex-col sm:flex-row gap-8 items-center bg-card border print:border-gray-300 p-6 rounded-lg">
              <div className="w-full sm:w-1/2">
                <RiskIndicator score={94} showLabel={false} className="mb-2" />
                <p className="text-center text-xs font-semibold uppercase text-destructive print:text-black mt-2">Critical Threat</p>
              </div>
              <div className="w-full sm:w-1/2">
                <h4 className="font-semibold text-sm mb-1">Assessment Engine Output</h4>
                <p className="text-sm text-muted-foreground print:text-gray-700">
                  Calculated score heavily influenced by heuristic overlap with known credential harvesting kits and deceptive domain structuring.
                </p>
              </div>
            </div>
          </section>

          {/* Technical Indicators */}
          <section className="space-y-4">
            <h3 className="text-lg font-bold border-b pb-2 uppercase tracking-wide print:border-gray-300">Technical Indicators of Compromise (IoCs)</h3>
            <div className="space-y-3">
              <div className="flex gap-3 text-sm">
                <AlertTriangle className="h-5 w-5 text-destructive shrink-0" />
                <div>
                  <span className="font-semibold block mb-1">Brand Impersonation (Heuristic)</span>
                  <span className="text-muted-foreground print:text-gray-700">The domain visually mimics a financial organization using hyphenated keyword stuffing, bypassing basic filters while tricking human operators.</span>
                </div>
              </div>
              <div className="flex gap-3 text-sm">
                <AlertTriangle className="h-5 w-5 text-destructive shrink-0" />
                <div>
                  <span className="font-semibold block mb-1">Suspicious URI Path</span>
                  <span className="text-muted-foreground print:text-gray-700">The path &apos;/login&apos; combined with the root domain has a 98% correlation with malicious phishing frameworks observed in the wild.</span>
                </div>
              </div>
              <div className="flex gap-3 text-sm">
                <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0" />
                <div>
                  <span className="font-semibold block mb-1">Infrastructure Reputation</span>
                  <span className="text-muted-foreground print:text-gray-700">The resolved IP address block has a historically poor reputation, hosting 14 other domains flagged in the past 30 days.</span>
                </div>
              </div>
            </div>
          </section>

          {/* Remediation */}
          <section className="space-y-4">
            <h3 className="text-lg font-bold border-b pb-2 uppercase tracking-wide print:border-gray-300">Recommended Remediation</h3>
            <div className="bg-destructive/10 print:bg-gray-100 border border-destructive/20 print:border-gray-300 p-4 rounded-md">
              <ul className="list-disc pl-5 space-y-2 text-sm">
                <li>Immediately blackhole the IP <code>192.0.2.144</code> on the edge firewall.</li>
                <li>Add the domain <code>paypal-verify-auth.com</code> to the internal DNS sinkhole.</li>
                <li>Force a password reset for any user who interacted with this URL within the last 24 hours.</li>
                <li>Forward the IoCs to the external threat sharing platform (STIX/TAXII).</li>
              </ul>
            </div>
          </section>

        </CardContent>
      </Card>

      {/* Print styles injection */}
      <style dangerouslySetInnerHTML={{__html: `
        @media print {
          body { background: white; color: black; }
          .dark { background: white; color: black; }
        }
      `}} />
    </div>
  )
}
