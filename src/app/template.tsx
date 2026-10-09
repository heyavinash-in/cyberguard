export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <div className="animate-in fade-in slide-in-from-bottom-2 duration-500 ease-in-out fill-mode-both h-full">
      {children}
    </div>
  )
}
