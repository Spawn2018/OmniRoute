import { useEffect, useState, type ReactNode } from "react"
import { useRouterState } from "@tanstack/react-router"
import { CommandPalette } from "@/components/command-palette"
import { Sidebar } from "@/components/layout/sidebar"

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname })
  const [paletteOpen, setPaletteOpen] = useState(false)

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault()
        setPaletteOpen((open) => !open)
      }
      if (event.key === "Escape") {
        setPaletteOpen(false)
      }
    }
    window.addEventListener("keydown", onKeyDown)
    return () => window.removeEventListener("keydown", onKeyDown)
  }, [])

  return (
    <div className="flex h-full min-h-0">
      <Sidebar currentPath={pathname} />
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-10 items-center justify-between border-b border-border bg-card px-4">
          <h1 className="text-sm font-medium">Platforma spedycyjna</h1>
          <button
            type="button"
            className="rounded-md border border-border px-2 py-1 text-xs text-muted-foreground hover:bg-muted"
            onClick={() => setPaletteOpen(true)}
          >
            Szukaj ⌘K
          </button>
        </header>
        <main className="min-h-0 flex-1 overflow-auto p-4">{children}</main>
      </div>
      <CommandPalette open={paletteOpen} onOpenChange={setPaletteOpen} />
    </div>
  )
}
