"use client"

import * as React from "react"
import { Sidebar } from "./sidebar"
import { Header } from "./header"

import { usePathname } from "next/navigation"

export function AppShell({ children }: { children: React.ReactNode }) {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)
  const pathname = usePathname()

  return (
    <div 
      className="flex h-screen w-full overflow-hidden text-foreground bg-cover bg-center bg-fixed"
      style={{ backgroundImage: 'url("/bg.jpg")' }}
    >
      <div className="absolute inset-0 bg-black/40 pointer-events-none z-0"></div>
      
      {/* Desktop Sidebar */}
      <Sidebar className="hidden md:flex relative z-10" />

      {/* Mobile Sidebar Overlay */}
      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}
      
      {/* Mobile Sidebar */}
      <div 
        className={`fixed inset-y-0 left-0 z-50 w-64 transform bg-card transition-transform duration-200 ease-in-out md:hidden ${
          mobileMenuOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <Sidebar className="flex w-full" onMobileClose={() => setMobileMenuOpen(false)} />
      </div>

      <div className="flex-1 flex flex-col min-w-0 h-full">
        <Header onMenuClick={() => setMobileMenuOpen(true)} />
        <main className="flex-1 overflow-auto p-4 md:p-6 lg:p-8 relative">
          {children}
        </main>
      </div>
    </div>
  )
}
