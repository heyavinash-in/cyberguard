import Link from 'next/link'
import { ShieldAlert } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[60vh] text-center space-y-6">
      <div className="h-24 w-24 rounded-full bg-destructive/10 flex items-center justify-center mb-4 relative">
        <div className="absolute inset-0 rounded-full animate-ping bg-destructive/20" />
        <ShieldAlert className="h-12 w-12 text-destructive relative z-10" />
      </div>
      <h2 className="text-3xl font-bold tracking-tight">404 - Access Denied</h2>
      <p className="text-muted-foreground max-w-md">
        The requested resource could not be located in the current environment, or you lack sufficient clearance to view this sector.
      </p>
      <Button asChild size="lg" className="mt-4">
        <Link href="/">Return to Dashboard</Link>
      </Button>
    </div>
  )
}
