"use client"

import { useState, useRef } from "react"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { RiskIndicator } from "@/components/ui/risk-indicator"
import { 
  ShieldAlert, 
  RefreshCw,
  Loader2,
  UploadCloud,
  FileImage,
  Info,
  SearchCode,
  AlertTriangle,
  FileWarning,
  CheckCircle2,
  ShieldCheck,
  Zap,
  Activity,
  Box,
  Fingerprint
} from "lucide-react"

const LOADING_STEPS = [
  "Extracting EXIF and file metadata...",
  "Applying multi-channel noise residual filters...",
  "Executing 2D Fast Fourier Transform (FFT)...",
  "Analyzing compression and texture artifacts...",
  "Processing through ViT neural classifier...",
  "Fusing model probability with forensic evidence..."
]

export default function MediaAnalyzerPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [status, setStatus] = useState<"idle" | "analyzing" | "complete">("idle")
  const [stepIndex, setStepIndex] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  const [result, setResult] = useState<any>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0]
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
    }
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return

    setStatus("analyzing")
    setStepIndex(0)
    setError(null)

    // Simulate step progress for UX
    let currentStep = 0
    const interval = setInterval(() => { currentStep++; if (currentStep < LOADING_STEPS.length) { setStepIndex(currentStep); } }, 200)

    try {
      const formData = new FormData()
      formData.append("image", selectedFile)

      const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/api/v1/media/image/analyze`, {
        method: "POST",
        body: formData,
      })

      clearInterval(interval)
      setStepIndex(LOADING_STEPS.length - 1)

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      if (!data.success) {
        throw new Error(data.error || "Analysis failed")
      }

      setResult(data)
      setStatus("complete")
    } catch (err: any) {
      clearInterval(interval)
      setError(err.message || "An error occurred during analysis")
      setStatus("idle")
    }
  }

  const resetAnalysis = () => {
    setStatus("idle")
    setSelectedFile(null)
    if (previewUrl) URL.revokeObjectURL(previewUrl)
    setPreviewUrl(null)
    setStepIndex(0)
    setResult(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Image Deepfake Detection</h1>
        <p className="text-muted-foreground">
          Upload an image to detect AI-generated content using our ViT classifier and frequency-domain forensics engine.
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
        <Card className="border-primary/20 bg-card">
          <CardHeader>
            <CardTitle>Upload Image for Authenticity Analysis</CardTitle>
            <CardDescription>Supported formats: JPG, PNG, WEBP (Max 10MB)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col md:flex-row gap-6">
              <div className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-muted-foreground/25 rounded-lg p-12 bg-background/50 hover:bg-accent/30 transition-colors">
                <UploadCloud className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-base font-medium mb-1">
                  {selectedFile ? selectedFile.name : "Drag & drop your image here"}
                </p>
                <p className="text-sm text-muted-foreground mb-6">
                  {selectedFile ? `${(selectedFile.size / 1024 / 1024).toFixed(2)} MB` : "or click to browse from your computer"}
                </p>
                
                <input 
                  type="file" 
                  accept="image/jpeg, image/png, image/webp"
                  className="hidden" 
                  ref={fileInputRef}
                  onChange={handleFileChange}
                />
                
                <div className="flex gap-4">
                  <Button variant="outline" onClick={() => fileInputRef.current?.click()}>
                    {selectedFile ? "Change Image" : "Select Image"}
                  </Button>
                  {selectedFile && (
                    <Button onClick={handleAnalyze}>
                      <SearchCode className="mr-2 h-4 w-4" /> Analyze Authenticity
                    </Button>
                  )}
                </div>
              </div>
              
              {previewUrl && (
                <div className="w-full md:w-64 shrink-0 rounded-lg overflow-hidden border border-muted-foreground/20 flex items-center justify-center bg-black/5">
                  <img src={previewUrl} alt="Preview" className="max-w-full max-h-64 object-contain" />
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {status === "analyzing" && (
        <Card className="border-primary/20 bg-primary/5">
          <CardContent className="pt-6 flex flex-col items-center justify-center min-h-[300px] space-y-8">
            <div className="relative">
              <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl animate-pulse" />
              <Loader2 className="h-16 w-16 animate-spin text-primary relative z-10" />
            </div>
            <div className="space-y-2 text-center w-full max-w-md">
              <h3 className="text-xl font-semibold">Inspecting Artifacts</h3>
              <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                <div 
                  className="h-full bg-primary transition-all duration-300 ease-out"
                  style={{ width: `${((stepIndex + 1) / LOADING_STEPS.length) * 100}%` }}
                />
              </div>
              <p className="text-muted-foreground text-sm h-6 animate-pulse">
                {LOADING_STEPS[stepIndex]}
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {status === "complete" && result && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="flex flex-col sm:flex-row justify-between gap-4">
            
            {result.classification === "AI_GENERATED" && (
              <Alert variant="destructive" className="flex-1 bg-destructive/10 border-destructive/30">
                <FileWarning className="h-5 w-5" />
                <AlertTitle className="text-lg flex items-center gap-2">SYNTHETIC MEDIA DETECTED</AlertTitle>
                <AlertDescription className="mt-2 text-base">The image exhibits high structural similarity to AI-generated content.</AlertDescription>
              </Alert>
            )}
            {result.classification === "REAL" && (
              <Alert className="flex-1 bg-emerald-500/10 border-emerald-500/30 text-emerald-500">
                <ShieldCheck className="h-5 w-5 text-emerald-500" />
                <AlertTitle className="text-lg flex items-center gap-2">AUTHENTIC CAMERA IMAGE</AlertTitle>
                <AlertDescription className="mt-2 text-base text-emerald-500/90">No synthetic structural anomalies detected.</AlertDescription>
              </Alert>
            )}
            {result.classification === "UNCERTAIN" && (
              <Alert className="flex-1 bg-amber-500/10 border-amber-500/30 text-amber-500">
                <AlertTriangle className="h-5 w-5 text-amber-500" />
                <AlertTitle className="text-lg flex items-center gap-2">UNCERTAIN ORIGIN</AlertTitle>
                <AlertDescription className="mt-2 text-base text-amber-500/90">Forensic signals and model confidence are ambiguous. Could be heavily edited art or a highly compressed image.</AlertDescription>
              </Alert>
            )}

            <Button variant="outline" size="lg" onClick={resetAnalysis} className="shrink-0 h-auto py-4">
              <RefreshCw className="mr-2 h-4 w-4" /> New Analysis
            </Button>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Evidence Fusion Analysis</CardTitle>
                <CardDescription>Processed in {result.model.inference_ms}ms using {result.model.name}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-8">
                
                {previewUrl && (
                  <div className="w-full rounded-lg overflow-hidden border border-muted-foreground/20 bg-black/5 flex justify-center py-4">
                    <img src={previewUrl} alt="Analyzed Media" className="max-h-64 object-contain rounded" />
                  </div>
                )}
                
                <div className="space-y-4">
                  <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground border-b pb-2">Forensic Signals & Evidence</h4>
                  <ul className="space-y-4">
                    {result.evidence.map((ind: any, i: number) => {
                      let Icon = Info;
                      if (ind.type === "MODEL_SIGNAL") Icon = Zap;
                      else if (ind.type === "FREQUENCY_SIGNAL") Icon = Activity;
                      else if (ind.type === "IMAGE_METADATA") Icon = Fingerprint;
                      else if (ind.type === "NOISE_SIGNAL") Icon = Box;

                      return (
                        <li key={i} className="flex items-start gap-3 text-sm bg-muted/30 p-3 rounded-lg border border-border/50">
                          <Icon className={`h-5 w-5 shrink-0 mt-0.5 ${ind.severity === 'HIGH' ? 'text-destructive' : ind.severity === 'MEDIUM' ? 'text-amber-500' : ind.severity === 'SAFE' ? 'text-emerald-500' : 'text-blue-500'}`} />
                          <div>
                            <div className="flex items-center gap-2">
                              <strong className="text-foreground">{ind.type.replace(/_/g, ' ')}</strong>
                              <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                                ind.strength === "STRONG" ? "bg-destructive/20 text-destructive" :
                                ind.strength === "MODERATE" ? "bg-amber-500/20 text-amber-500" :
                                ind.strength === "WEAK" ? "bg-blue-500/20 text-blue-500" :
                                "bg-emerald-500/20 text-emerald-500"
                              }`}>
                                {ind.strength}
                              </span>
                            </div>
                            <p className="text-muted-foreground mt-1 leading-relaxed">{ind.description}</p>
                            <p className="text-xs text-muted-foreground/50 mt-1 flex justify-between">
                              <span>Source: {ind.source}</span>
                            </p>
                          </div>
                        </li>
                      )
                    })}
                  </ul>
                </div>
                
                {/* Technical Forensics Breakdown */}
                {result.forensics && (
                  <div className="grid grid-cols-2 gap-4 mt-6 text-xs">
                    <div className="p-3 bg-muted/40 rounded border border-border">
                      <strong className="block mb-2 text-muted-foreground uppercase">Frequency (FFT)</strong>
                      <div className="flex justify-between"><span>High Freq Energy:</span> <span>{(result.forensics.frequency?.high_frequency_ratio * 100).toFixed(1)}%</span></div>
                      <div className="flex justify-between"><span>Anomaly:</span> <span>{result.forensics.frequency?.frequency_anomaly}</span></div>
                    </div>
                    <div className="p-3 bg-muted/40 rounded border border-border">
                      <strong className="block mb-2 text-muted-foreground uppercase">Noise / Texture</strong>
                      <div className="flex justify-between"><span>Noise Residual (Mean):</span> <span>{result.forensics.noise?.noise_mean?.toFixed(2) || "N/A"}</span></div>
                      <div className="flex justify-between"><span>Anomaly:</span> <span>{result.forensics.noise?.noise_anomaly}</span></div>
                    </div>
                  </div>
                )}

              </CardContent>
            </Card>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Cyber Risk Score</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <RiskIndicator score={result.risk_score} />
                  
                  <div className="space-y-3 pt-4 border-t">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-muted-foreground">AI Probability</span>
                      <span className="font-mono font-medium">{(result.ai_probability * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-muted-foreground">Real Probability</span>
                      <span className="font-mono font-medium">{(result.real_probability * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-muted-foreground">Network Confidence</span>
                      <span className="font-mono font-medium text-primary">{(result.confidence * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-muted/30">
                <CardHeader>
                  <CardTitle className="text-sm uppercase tracking-wider text-muted-foreground">File Metadata</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Format</span>
                    <span className="font-mono">{result.metadata.format}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Dimensions</span>
                    <span className="font-mono">{result.metadata.width}x{result.metadata.height}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Color Mode</span>
                    <span className="font-mono">{result.metadata.mode}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">EXIF Present</span>
                    <span className="font-mono">{result.metadata.has_exif ? "Yes" : "No"}</span>
                  </div>
                  <div className="flex flex-col mt-2 pt-2 border-t border-border/50">
                    <span className="text-muted-foreground mb-1">SHA-256</span>
                    <span className="font-mono text-[10px] break-all">{result.metadata.sha256}</span>
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
