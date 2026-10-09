"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Link as LinkIcon,
  Mail,
  FileImage,
  ShieldCheck,
  ShieldAlert,
  Search,
  Activity,
  Server,
  ActivitySquare
} from "lucide-react"

const navItems: any[] = [
  {
    name: "COMMAND CENTER",
    items: [
      { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
    ],
  },
  {
    name: "DETECTION",
    items: [
      { name: "URL Scanner", href: "/analyze/url", icon: LinkIcon },
      { name: "Message Scanner", href: "/analyze/message", icon: Mail },
      { name: "Media Intelligence", href: "/analyze/media", icon: FileImage },
      { name: "Account Security", href: "/account-security", icon: ShieldAlert },
    ],
  },
  {
    name: "INVESTIGATION",
    items: [
      { name: "Threat Cases", href: "/threat-cases", icon: Search },
      { name: "Activity Timeline", href: "/activity", icon: Activity },
    ],
  },
  {
    name: "SYSTEM",
    items: [
      { name: "Models & Engines", href: "/models", icon: Server },
      { name: "System Health", href: "/system-health", icon: ActivitySquare },
    ],
  },
]

export function Sidebar({ className, onMobileClose }: { className?: string, onMobileClose?: () => void }) {
  const pathname = usePathname()

  return (
    <aside
      className={cn(
        "flex flex-col border-r border-white/20 bg-white/10 backdrop-blur-xl transition-all duration-300 ease-in-out shadow-[0_4px_30px_rgba(0,0,0,0.1)] relative z-20",
        "w-64 md:w-[72px] lg:w-64", 
        "px-4 md:px-2 lg:px-4 py-6 text-white",
        className
      )}
    >
      <div className="flex items-center gap-2 px-2 mb-8 justify-center lg:justify-start">
        <ShieldCheck className="h-8 w-8 shrink-0 text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.8)]" />
        <span className="text-xl font-bold tracking-tight md:hidden lg:block whitespace-nowrap overflow-hidden text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]">
          CyberGuard
        </span>
      </div>

      <nav className="flex-1 space-y-6 overflow-y-auto overflow-x-hidden scrollbar-none">
        {navItems.map((group, i) => {
          if (group.items) {
            return (
              <div key={i} className="space-y-2">
                <h4 className="px-2 text-xs font-semibold uppercase tracking-wider text-white/60 md:hidden lg:block whitespace-nowrap overflow-hidden">
                  {group.name}
                </h4>
                <div className="md:block lg:hidden text-center mb-2">
                  <div className="h-[1px] w-6 bg-white/20 mx-auto" />
                </div>
                <div className="space-y-1">
                  {group.items.map((item: any) => {
                    const isActive = pathname === item.href
                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        onClick={onMobileClose}
                        title={item.name}
                        className={cn(
                          "flex items-center gap-3 rounded-xl px-2 py-3 md:py-2 lg:py-3 text-sm font-medium transition-all md:justify-center lg:justify-start",
                          isActive
                            ? "bg-white/20 text-white shadow-[0_4px_30px_rgba(0,0,0,0.1)] border border-white/20"
                            : "text-white/70 hover:bg-white/10 hover:text-white"
                        )}
                      >
                        <item.icon className="h-5 w-5 shrink-0" />
                        <span className="md:hidden lg:block whitespace-nowrap overflow-hidden">
                          {item.name}
                        </span>
                      </Link>
                    )
                  })}
                </div>
              </div>
            )
          }

          const isActive = pathname === group.href
          return (
            <div key={i} className="space-y-1">
              <Link
                href={group.href}
                onClick={onMobileClose}
                title={group.name}
                className={cn(
                  "flex items-center gap-3 rounded-xl px-2 py-3 md:py-2 lg:py-3 text-sm font-medium transition-all md:justify-center lg:justify-start",
                  isActive
                    ? "bg-white/20 text-white shadow-[0_4px_30px_rgba(0,0,0,0.1)] border border-white/20"
                    : "text-white/70 hover:bg-white/10 hover:text-white"
                )}
              >
                {group.icon && <group.icon className="h-5 w-5 shrink-0" />}
                <span className="md:hidden lg:block whitespace-nowrap overflow-hidden">
                  {group.name}
                </span>
              </Link>
            </div>
          )
        })}
      </nav>
    </aside>
  )
}
