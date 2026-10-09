"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Shield, Radar, Zap, ShieldCheck, Terminal, Search, Link as LinkIcon, Mail, FileCode, FileImage } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function InteractiveHubPage() {
  const router = useRouter();
  const [scanMode, setScanMode] = useState<"url" | "text" | "raw">("url");
  const [scanInput, setScanInput] = useState("");

  const handleLaunch = () => {
    if (scanMode !== "raw" && !scanInput.trim()) return;
    if (scanMode === "url") {
      router.push(`/analyze/url?q=${encodeURIComponent(scanInput)}`);
    } else if (scanMode === "text") {
      router.push(`/analyze/message?q=${encodeURIComponent(scanInput)}`);
    } else {
      router.push(`/analyze/media`);
    }
  };

  return (
    <div className="flex flex-col gap-8 w-full max-w-7xl mx-auto min-h-[calc(100vh-8rem)] justify-center">
      
      {/* TOP OPERATIONAL BAR */}
      <div className="w-full bg-white/10 backdrop-blur-xl rounded-xl p-4 flex flex-wrap items-center justify-between gap-4 shadow-md border border-white/20">
        <div className="flex items-center gap-6 flex-wrap">
          <div className="flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500 animate-ping"></span>
            <div className="flex flex-col">
              <span className="text-[10px] text-white/60 uppercase tracking-wider">NEURAL WEIGHTS</span>
              <span className="text-xs text-blue-400 font-medium">Llama-3-Guard-8B [INT8 • 1.8GB VRAM]</span>
            </div>
          </div>
          <div className="h-6 w-px bg-white/10 hidden md:block"></div>
          <div className="flex items-center gap-3">
            <ShieldCheck className="text-emerald-500 h-5 w-5" />
            <div className="flex flex-col">
              <span className="text-[10px] text-white/60 uppercase tracking-wider">AIRGAP ISOLATION</span>
              <span className="text-xs text-emerald-400 font-medium">100% SECURE • 0 BYTES EXFIL</span>
            </div>
          </div>
          <div className="h-6 w-px bg-white/10 hidden lg:block"></div>
          <div className="flex items-center gap-3">
            <Zap className="text-purple-400 h-5 w-5" />
            <div className="flex flex-col">
              <span className="text-[10px] text-white/60 uppercase tracking-wider">INFERENCE LATENCY</span>
              <span className="text-xs text-purple-400 font-medium">8.4ms / token [Metal GPU]</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full bg-white/20 text-white/60 text-[10px] font-semibold">NODE: ALPHA-7</span>
          <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-[10px] font-semibold">ONLINE</span>
        </div>
      </div>

      {/* HERO HUD INTERACTION MATRIX */}
      <div className="relative w-full rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 overflow-hidden p-8 md:p-12 shadow-2xl flex flex-col lg:flex-row gap-12 items-center justify-between">
        
        {/* Ambient Radial Cyber Scrim */}
        <div className="absolute -right-20 -top-20 w-96 h-96 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none"></div>
        <div className="absolute -left-20 -bottom-20 w-96 h-96 rounded-full bg-blue-500/10 blur-3xl pointer-events-none"></div>
        
        {/* Left Column: Tactical Control & Quick Scanner */}
        <div className="flex flex-col gap-6 max-w-xl z-10 w-full">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-[10px] tracking-widest uppercase font-bold">TACTICAL COMMAND // CORE</span>
            <span className="text-white/60 text-[10px]">SYS.VER.2.4.9</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl lg:text-6xl text-white font-bold tracking-tight">
            Local-First Neural <br/>
            <span className="text-emerald-400 drop-shadow-[0_0_15px_rgba(16,185,129,0.3)]">Autonomous Defense</span>
          </h1>
          
          <p className="text-white/80 text-sm md:text-base leading-relaxed">
            Sub-millisecond deep payload heuristic inspection, authority spoof intercept, and deterministic neural sandboxing executed strictly on bare metal.
          </p>
          
          {/* Launchpad Inset Terminal Form */}
          <div className="mt-4 bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-5 shadow-inner flex flex-col gap-4">
            
            {/* Scan Payload Type Switcher */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex items-center gap-1 p-1 bg-white/5 backdrop-blur-md rounded-lg">
                <button 
                  onClick={() => setScanMode("url")}
                  className={`px-3 py-1.5 rounded text-xs transition-all font-medium flex items-center gap-2 ${scanMode === "url" ? "bg-emerald-500/20 text-emerald-400" : "text-white/80 hover:text-white"}`}
                >
                  <LinkIcon className="h-3 w-3" /> URL Probe
                </button>
                <button 
                  onClick={() => setScanMode("text")}
                  className={`px-3 py-1.5 rounded text-xs transition-all font-medium flex items-center gap-2 ${scanMode === "text" ? "bg-emerald-500/20 text-emerald-400" : "text-white/80 hover:text-white"}`}
                >
                  <Mail className="h-3 w-3" /> Semantic Msg
                </button>
                <button 
                  onClick={() => setScanMode("raw")}
                  className={`px-3 py-1.5 rounded text-xs transition-all font-medium flex items-center gap-2 ${scanMode === "raw" ? "bg-emerald-500/20 text-emerald-400" : "text-white/80 hover:text-white"}`}
                >
                  <FileImage className="h-3 w-3" /> Image Check
                </button>
              </div>
              <span className="text-[10px] text-blue-400 flex items-center gap-2 font-bold tracking-wider">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span> AIRGAP READY
              </span>
            </div>
            
            {/* Input Box */}
            <div className="relative flex items-center">
              <Search className="absolute left-3 text-white/60 h-5 w-5" />
              <input 
                className="w-full bg-white/5 backdrop-blur-md text-white text-sm pl-10 pr-32 py-4 rounded-lg focus:outline-none focus:ring-1 focus:ring-emerald-500 shadow-sm placeholder:text-white/40 border border-white/20" 
                placeholder={scanMode === "url" ? "https://secure-login.portal-update.internal.app/auth" : scanMode === "text" ? "Paste email or SMS body here..." : "Click INSPECT to upload an image..."}
                type="text"
                value={scanInput}
                onChange={(e) => setScanInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleLaunch()}
              />
              <button 
                onClick={handleLaunch}
                className="absolute right-2 px-4 py-2 rounded bg-emerald-500 text-black text-xs font-bold hover:bg-emerald-400 transition-all flex items-center gap-2 shadow-md" 
                type="button"
              >
                <span>INSPECT</span>
                <Radar className="h-4 w-4" />
              </button>
            </div>
            
            {/* Diagnostic Micro Telemetry Trace */}
            <div className="flex items-center justify-between text-white/60 text-[10px] uppercase font-semibold">
              <span>Engine state: idle • Vector weights loaded in memory</span>
              <span className="font-mono text-white/80 tracking-widest">CRTL + ENTER TO DETECT</span>
            </div>
          </div>
        </div>
        
        {/* Right Column: Animated Holographic Radar HUD */}
        <div className="relative flex items-center justify-center w-full lg:w-96 h-80 z-10 select-none">
          <svg className="w-72 h-72 md:w-80 md:h-80 drop-shadow-[0_0_20px_rgba(16,185,129,0.2)]" fill="none" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <path className="fill-slate-900/60" d="M100 12 L164 42 V108 C164 150 100 188 100 188 C100 188 36 150 36 108 V42 L100 12 Z"></path>
            <path className="stroke-emerald-500" d="M100 16 L158 44 V106 C158 144 100 180 100 180 C100 180 42 144 42 106 V44 L100 16 Z" strokeLinejoin="round" strokeWidth="6"></path>
            <path className="stroke-blue-500" d="M100 28 L146 50 V102 C146 134 100 166 100 166 C100 166 54 134 54 102 V50 L100 28 Z" strokeDasharray="6 7" strokeLinecap="round" strokeWidth="4"></path>
            <circle className="fill-slate-800/70" cx="100" cy="104" r="42"></circle>
            <circle className="stroke-emerald-500/50" cx="100" cy="104" r="38" strokeWidth="2"></circle>
            <circle className="stroke-emerald-500" cx="100" cy="104" r="26" strokeWidth="3"></circle>
            <path className="stroke-white/80" d="M85 104 L115 104 M100 89 L100 119" strokeWidth="2"></path>
            <circle className="stroke-white/20" cx="100" cy="104" r="60" strokeWidth="1" strokeDasharray="2 4"></circle>
          </svg>
        </div>
      </div>
    </div>
  );
}
