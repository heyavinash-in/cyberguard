import * as React from "react"
import { cn } from "@/lib/utils"

interface RiskIndicatorProps extends React.HTMLAttributes<HTMLDivElement> {
  score: number
  showLabel?: boolean
}

export function RiskIndicator({ score, showLabel = true, className, ...props }: RiskIndicatorProps) {
  // Determine risk level based on score
  let level = "SAFE"
  let color = "text-emerald-500"
  let bgColor = "bg-emerald-500"

  if (score > 80) {
    level = "CRITICAL"
    color = "text-red-500"
    bgColor = "bg-red-500"
  } else if (score > 60) {
    level = "HIGH"
    color = "text-orange-500"
    bgColor = "bg-orange-500"
  } else if (score > 40) {
    level = "MEDIUM"
    color = "text-yellow-500"
    bgColor = "bg-yellow-500"
  } else if (score > 20) {
    level = "LOW"
    color = "text-blue-500"
    bgColor = "bg-blue-500"
  }

  return (
    <div className={cn("flex flex-col gap-2", className)} {...props}>
      <div className="flex items-center justify-between text-sm">
        <span className="font-semibold text-muted-foreground">Risk Score</span>
        <span className={cn("font-bold", color)}>{score}/100</span>
      </div>
      <div className="h-2 w-full rounded-full bg-secondary overflow-hidden">
        <div 
          className={cn("h-full rounded-full transition-all duration-1000 ease-out", bgColor)}
          style={{ width: `${Math.max(2, score)}%` }}
        />
      </div>
      {showLabel && (
        <div className="flex justify-between text-xs text-muted-foreground mt-1">
          <span>Safe (0-20)</span>
          <span>Critical (81-100)</span>
        </div>
      )}
    </div>
  )
}
