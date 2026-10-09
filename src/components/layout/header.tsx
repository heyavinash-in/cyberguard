import { Menu, Bell, User, Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function Header({ onMenuClick }: { onMenuClick?: () => void }) {
  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-white/20 bg-white/10 px-4 backdrop-blur-xl shadow-[0_4px_30px_rgba(0,0,0,0.1)] md:px-6 safe-area-pt relative z-10">
      <div className="flex items-center gap-4">
        {/* Mobile menu trigger - hidden on md */}
        <Button variant="ghost" size="icon" className="md:hidden h-11 w-11 shrink-0 text-white hover:bg-white/20" onClick={onMenuClick}>
          <Menu className="h-6 w-6" />
          <span className="sr-only">Toggle Menu</span>
        </Button>
        
        {/* Search */}
        <div className="hidden max-w-sm flex-1 sm:flex items-center relative">
          <Search className="absolute left-2.5 h-4 w-4 text-white/50" />
          <Input
            type="search"
            placeholder="Search indicators, IP, hashes..."
            className="w-[200px] md:w-[300px] lg:w-[400px] pl-9 bg-white/5 border border-white/10 text-white placeholder:text-white/50 focus-visible:bg-white/10 focus-visible:ring-white/30 transition-all shadow-[0_4px_30px_rgba(0,0,0,0.1)] backdrop-blur-md"
          />
        </div>
      </div>

      <div className="flex items-center gap-2 md:gap-4">
        {/* Notifications */}
        <Button variant="ghost" size="icon" className="relative h-11 w-11 md:h-10 md:w-10 shrink-0 text-white hover:bg-white/20 hover:text-white">
          <Bell className="h-5 w-5" />
          <span className="absolute top-2 right-2.5 h-2 w-2 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.8)] border-none" />
          <span className="sr-only">Notifications</span>
        </Button>
        
        {/* User Profile */}
        <Button variant="ghost" size="icon" className="rounded-full bg-white/10 border border-white/20 h-11 w-11 md:h-10 md:w-10 shrink-0 text-white hover:bg-white/20 shadow-[0_4px_30px_rgba(0,0,0,0.1)]">
          <User className="h-5 w-5" />
          <span className="sr-only">User Profile</span>
        </Button>
      </div>
    </header>
  )
}
