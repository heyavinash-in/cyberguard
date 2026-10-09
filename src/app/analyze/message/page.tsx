"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Radar, Mail, AlertTriangle, ShieldCheck, Activity, CheckCircle2, FileCode } from "lucide-react";

function MessageScannerContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("q");

  const [message, setMessage] = useState(initialQuery || "");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleScan = async () => {
    if (!message.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/analyze-message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const json = await res.json();
      
      if (json.success) {
        const factors = json.data.riskFactors || [];
        const factorTitles = factors.map((f: any) => f.title || f.type || "Threat Vector");

        setResult({
          risk: json.data.riskScore,
          categories: factorTitles,
          details: json.data.explanation,
          recommendation: json.data.recommendation,
          mlUsed: json.meta?.mlUsed
        });
      } else {
        setResult({ risk: 0, categories: ["ERROR"], details: json.error?.message || "Failed to analyze message.", recommendation: "" });
      }
    } catch (e) {
      console.error(e);
      setResult({ risk: 0, categories: ["ERROR"], details: "Server connection failed.", recommendation: "" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialQuery) {
      handleScan();
    }
  }, [initialQuery]);

  return (
    <div className="flex flex-col gap-8 w-full max-w-6xl mx-auto pt-4 pb-12">
      
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-purple-500 animate-ping"></span>
            <span className="text-[10px] text-purple-400 uppercase tracking-widest font-bold">SECURITY MODULE</span>
          </div>
          <div className="flex items-baseline gap-4">
            <h1 className="text-3xl font-bold text-white tracking-tight">Message Analysis</h1>
          </div>
          <p className="text-sm text-white/70 max-w-2xl mt-1">
            Scan emails, SMS text, or raw message payloads for social engineering and spear-phishing attacks.
          </p>
        </div>
      </div>

      {/* Input Section */}
      <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 flex flex-col gap-6 relative overflow-hidden border border-white/20 shadow-[0_8px_32px_rgba(0,0,0,0.3)]">
        
        <div className="flex flex-wrap items-center justify-between gap-4 z-10">
          <div className="flex items-center gap-2">
            <Mail className="text-purple-400 h-5 w-5" />
            <span className="text-xs text-white uppercase font-bold tracking-wider">Input Message</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] text-white/50 mr-1 font-semibold uppercase">EXAMPLES:</span>
            <button onClick={() => setMessage("URGENT: Your account will be suspended in 24 hours. Click here to verify your identity immediately.")} className="px-2 py-1 bg-white/5 hover:bg-white/10 text-white/80 border border-white/10 text-[10px] rounded transition-colors font-mono">
              urgency-phish.txt
            </button>
            <button onClick={() => setMessage("Hey team, just attaching the notes from today's sync. Let me know if you need anything else.")} className="px-2 py-1 bg-white/5 hover:bg-white/10 text-white/80 border border-white/10 text-[10px] rounded transition-colors font-mono">
              benign-email.txt
            </button>
          </div>
        </div>

        <div className="flex flex-col gap-4 items-stretch z-10">
          <div className="relative flex-1">
            <textarea 
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full h-48 bg-black/40 text-white font-mono text-sm p-4 rounded-xl focus:outline-none focus:ring-1 focus:ring-purple-500 border border-white/20 shadow-inner resize-none placeholder:text-white/30" 
              placeholder="Paste email body, SMS text, or raw message payload here..." 
            />
            <div className="absolute bottom-4 right-4 flex items-center">
              <button 
                onClick={() => {
                  if (navigator.clipboard && navigator.clipboard.readText) {
                    navigator.clipboard.readText()
                      .then(text => setMessage(text))
                      .catch(err => console.warn("Clipboard access denied. Please paste manually.", err));
                  } else {
                    console.warn("Clipboard API not available.");
                  }
                }}
                className="flex items-center gap-1 px-3 py-1.5 bg-white/10 text-white/80 hover:text-white hover:bg-white/20 border border-white/10 rounded text-xs font-bold transition-colors shadow-sm"
              >
                PASTE FROM CLIPBOARD
              </button>
            </div>
          </div>
          
          <div className="flex justify-end">
            <button 
              disabled={loading}
              onClick={handleScan}
              className="relative flex items-center justify-center gap-2 px-8 py-4 bg-purple-500 hover:bg-purple-400 text-white font-bold text-sm rounded-xl transition-all shadow-[0_0_15px_rgba(168,85,247,0.3)] min-w-[200px]"
            >
              {loading ? <Radar className="h-5 w-5 animate-spin" /> : <Radar className="h-5 w-5" />}
              <span className="tracking-widest uppercase">{loading ? "SCANNING..." : "ANALYZE MESSAGE"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start mt-4 animate-in slide-in-from-bottom-8 duration-500">
          
          <div className="lg:col-span-5 flex flex-col gap-6">
            <div className={`bg-white/10 backdrop-blur-xl rounded-2xl p-6 flex flex-col gap-6 border shadow-[0_8px_32px_rgba(0,0,0,0.3)] ${result.risk >= 75 ? "border-red-500/50 shadow-[0_0_30px_rgba(239,68,68,0.2)]" : result.risk >= 40 ? "border-amber-500/50 shadow-[0_0_30px_rgba(245,158,11,0.2)]" : "border-emerald-500/50 shadow-[0_0_30px_rgba(16,185,129,0.2)]"}`}>
              <div className="flex items-center justify-between">
                <span className={`text-[10px] uppercase tracking-wider flex items-center gap-1 font-bold ${result.risk >= 75 ? "text-red-400" : result.risk >= 40 ? "text-amber-400" : "text-emerald-400"}`}>
                  {result.risk >= 75 ? <AlertTriangle className="h-4 w-4" /> : <ShieldCheck className="h-4 w-4" />}
                  {result.risk >= 75 ? "CRITICAL THREAT" : result.risk >= 40 ? "SUSPICIOUS" : "SAFE / BENIGN"}
                </span>
                <span className="text-[10px] text-white/50 font-mono">THREAT SCORE</span>
              </div>
              
              <div className="flex items-end gap-2">
                <span className={`text-7xl font-bold tracking-tighter ${result.risk >= 75 ? "text-red-400 drop-shadow-[0_0_15px_rgba(239,68,68,0.4)]" : result.risk >= 40 ? "text-amber-400 drop-shadow-[0_0_15px_rgba(245,158,11,0.4)]" : "text-emerald-400 drop-shadow-[0_0_15px_rgba(16,185,129,0.4)]"}`}>
                  {result.risk ?? 0}
                </span>
                <span className="text-2xl text-white/40 mb-2 font-light">/100</span>
              </div>
              
              <div className="w-full h-1.5 bg-black/40 rounded-full overflow-hidden">
                <div 
                  className={`h-full transition-all duration-1000 ease-out ${result.risk >= 75 ? "bg-red-500" : result.risk >= 40 ? "bg-amber-500" : "bg-emerald-500"}`}
                  style={{ width: `${result.risk ?? 0}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 shadow-[0_8px_32px_rgba(0,0,0,0.3)] flex flex-col gap-4">
              <span className="text-[10px] text-white/60 uppercase tracking-widest font-bold">Detected Threat Types</span>
              <div className="flex flex-wrap gap-2">
                {result.categories && result.categories.length > 0 ? (
                  result.categories.map((cat: string) => (
                    <span key={cat} className="px-3 py-1 bg-red-500/20 text-red-200 border border-red-500/30 rounded-md text-xs font-mono font-semibold">
                      {cat}
                    </span>
                  ))
                ) : (
                  <span className="px-3 py-1 bg-emerald-500/20 text-emerald-200 border border-emerald-500/30 rounded-md text-xs font-mono font-semibold flex items-center gap-1">
                    <CheckCircle2 className="h-3 w-3" /> NO THREATS FOUND
                  </span>
                )}
              </div>
            </div>
          </div>
          
          <div className="lg:col-span-7 bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-[0_8px_32px_rgba(0,0,0,0.3)] overflow-hidden flex flex-col h-full">
            <div className="bg-black/30 px-6 py-4 border-b border-white/10 flex items-center gap-3">
              <Activity className="text-purple-400 h-5 w-5" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">Analysis Details</h3>
            </div>
            
            <div className="p-6 flex-1 flex flex-col gap-6 text-sm text-white/80">
              
              <div>
                <h4 className="text-xs font-bold text-white/50 uppercase tracking-wider mb-2">Explanation</h4>
                <p className="leading-relaxed">
                  {result.details || "Telemetry analysis completed with no significant threat vectors."}
                </p>
              </div>

              {result.recommendation && (
                <div>
                  <h4 className="text-xs font-bold text-white/50 uppercase tracking-wider mb-2 mt-2">Recommended Action</h4>
                  <p className="text-emerald-200 bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-lg">
                    {result.recommendation}
                  </p>
                </div>
              )}

              <div className="flex items-center gap-4 text-xs font-mono text-white/40 mt-4 pt-4 border-t border-white/10">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-emerald-500 rounded-sm"></div>
                  <span>AI_ENGINE: {result.mlUsed ? "ACTIVE" : "INACTIVE"}</span>
                </div>
              </div>

            </div>
          </div>

        </div>
      )}

    </div>
  );
}

export default function MessageScannerPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-64 text-purple-500"><Radar className="animate-spin h-8 w-8" /></div>}>
      <MessageScannerContent />
    </Suspense>
  );
}
