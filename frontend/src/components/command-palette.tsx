import { useEffect, useState } from "react"
import { useNavigate } from "@tanstack/react-router"
import { Command } from "cmdk"
import { Search } from "lucide-react"
import { track } from "@/lib/analytics"
import { OPERATOR_ACTIONS, runOperatorAction } from "@/lib/operator-actions"
import { cn } from "@/lib/utils"

type CommandPaletteProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const NAV_ACTIONS = [
  { id: "nav-home", label: "Idź do pulpitu", to: "/" },
  { id: "nav-users", label: "Idź do użytkowników tenanta", to: "/tenancy/users" },
  { id: "nav-extractions", label: "Idź do kolejki ekstrakcji", to: "/extractions" },
  { id: "nav-charge-codes", label: "Idź do katalogu kodów opłat", to: "/charge-codes" },
  { id: "nav-charges", label: "Idź do opłat", to: "/charges" },
  { id: "nav-rate-lines", label: "Idź do stawek kupna", to: "/rate-lines" },
  { id: "nav-session", label: "Ustawienia sesji (tenant)", to: "/session" },
] as const

export function commandPaletteActionIds(): string[] {
  return [...NAV_ACTIONS.map((action) => action.id), ...OPERATOR_ACTIONS.map((action) => action.id)]
}

export function CommandPalette({ open, onOpenChange }: CommandPaletteProps) {
  const navigate = useNavigate()
  const [query, setQuery] = useState("")

  useEffect(() => {
    if (!open) {
      setQuery("")
    }
  }, [open])

  if (!open) {
    return null
  }

  return (
    <div className="fixed inset-0 z-50">
      <button
        type="button"
        className="absolute inset-0 bg-foreground/30"
        aria-label="Zamknij paletę"
        onClick={() => onOpenChange(false)}
      />
      <div className="relative mx-auto mt-[12vh] w-full max-w-lg rounded-md border border-border bg-card shadow-sm">
        <Command label="Paleta poleceń" shouldFilter>
          <div className="flex items-center gap-2 border-b border-border px-3">
            <Search className="size-4 text-muted-foreground" />
            <Command.Input
              value={query}
              onValueChange={setQuery}
              placeholder="Szukaj akcji…"
              className="h-10 w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground"
            />
          </div>
          <Command.List className="max-h-72 overflow-auto p-1">
            <Command.Empty className="px-3 py-6 text-center text-sm text-muted-foreground">
              Brak wyników
            </Command.Empty>
            <Command.Group heading="Nawigacja" className="px-1 py-1 text-xs text-muted-foreground">
              {NAV_ACTIONS.map((action) => (
                <Command.Item
                  key={action.id}
                  value={action.label}
                  className={cn(
                    "flex cursor-pointer items-center rounded-md px-2 py-1.5 text-sm text-foreground",
                    "data-[selected=true]:bg-muted",
                  )}
                  onSelect={() => {
                    track("command_palette_used", { action: action.id })
                    onOpenChange(false)
                    void navigate({ to: action.to })
                  }}
                >
                  {action.label}
                </Command.Item>
              ))}
            </Command.Group>
            <Command.Group heading="Akcje operatora" className="px-1 py-1 text-xs text-muted-foreground">
              {OPERATOR_ACTIONS.map((action) => (
                <Command.Item
                  key={action.id}
                  value={action.label}
                  className={cn(
                    "flex cursor-pointer items-center rounded-md px-2 py-1.5 text-sm text-foreground",
                    "data-[selected=true]:bg-muted",
                  )}
                  onSelect={() => {
                    track("command_palette_used", { action: action.id })
                    onOpenChange(false)
                    if (action.route) {
                      void navigate({ to: action.route })
                    }
                    runOperatorAction(action.id)
                  }}
                >
                  {action.label}
                </Command.Item>
              ))}
            </Command.Group>
          </Command.List>
        </Command>
      </div>
    </div>
  )
}
