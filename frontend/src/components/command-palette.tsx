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
  { id: "nav-finance", label: "Idź do tablicy finansowej", to: "/finance" },
  { id: "nav-invoices", label: "Idź do faktur", to: "/invoices" },
  { id: "nav-quote-invoices", label: "Idź do rozliczenia wyceny", to: "/quote-invoices" },
  { id: "nav-payments", label: "Idź do banku i płatności", to: "/payments" },
  { id: "nav-money-cost", label: "Idź do kosztu pieniądza", to: "/money-cost" },
  { id: "nav-fx-differences", label: "Idź do różnic kursowych", to: "/fx-differences" },
  { id: "nav-cashflows", label: "Idź do przepływów", to: "/cashflows" },
  { id: "nav-cost-to-serve", label: "Idź do kosztu obsługi klienta", to: "/cost-to-serve" },
  { id: "nav-bookkeeping", label: "Idź do księgowości", to: "/bookkeeping" },
  { id: "nav-road", label: "Idź do transportu drogowego", to: "/road" },
  { id: "nav-rail", label: "Idź do kolei intermodalnej", to: "/rail" },
  { id: "nav-china-rail", label: "Idź do kolei z Chin", to: "/china-rail" },
  { id: "nav-lcl", label: "Idź do drobnicy morskiej", to: "/lcl" },
  { id: "nav-sanctions", label: "Idź do sankcji", to: "/sanctions" },
  { id: "nav-fraud", label: "Idź do oszustwa", to: "/fraud" },
  { id: "nav-gdpr", label: "Idź do RODO", to: "/gdpr" },
  { id: "nav-ai", label: "Idź do propozycji AI", to: "/ai" },
  { id: "nav-health", label: "Idź do obserwowalności", to: "/health" },
  { id: "nav-quality", label: "Idź do jakości ekstrakcji", to: "/quality" },
  { id: "nav-rollout", label: "Idź do wdrożenia", to: "/rollout" },
  { id: "nav-mail", label: "Idź do tablicy poczty", to: "/mail" },
  { id: "nav-notifications", label: "Idź do powiadomień", to: "/notifications" },
  { id: "nav-outbox", label: "Idź do outbox", to: "/outbox" },
  { id: "nav-shipments", label: "Idź do zleceń", to: "/shipments" },
  { id: "nav-tracking", label: "Idź do trackingu", to: "/tracking" },
  { id: "nav-exceptions", label: "Idź do wyjątków", to: "/exceptions" },
  { id: "nav-claims", label: "Idź do reklamacji", to: "/claims" },
  { id: "nav-watchtower", label: "Idź do wieży", to: "/watchtower" },
  { id: "nav-shipment-documents", label: "Idź do dokumentów zlecenia", to: "/shipment-documents" },
  { id: "nav-edi", label: "Idź do EDI", to: "/edi" },
  { id: "nav-charge-codes", label: "Idź do katalogu kodów opłat", to: "/charge-codes" },
  { id: "nav-commodity-codes", label: "Idź do katalogu kodów towarowych", to: "/commodity-codes" },
  { id: "nav-dangerous-goods", label: "Idź do katalogu towarów niebezpiecznych", to: "/dangerous-goods" },
  { id: "nav-networks", label: "Idź do katalogu sieci", to: "/networks" },
  { id: "nav-party-scorecards", label: "Idź do kart wyników kontrahenta", to: "/party-scorecards" },
  { id: "nav-customer-sops", label: "Idź do procedur operacyjnych klienta", to: "/customer-sops" },
  { id: "nav-credit-reviews", label: "Idź do katalogu recenzji kredytowych", to: "/credit-reviews" },
  { id: "nav-decisions", label: "Idź do szyny decyzji operatora", to: "/decisions" },
  { id: "nav-port-surcharges", label: "Idź do katalogu extra portowych", to: "/port-surcharges" },
  { id: "nav-nbp-rates", label: "Idź do katalogu kursów NBP", to: "/nbp-rates" },
  { id: "nav-charges", label: "Idź do opłat", to: "/charges" },
  { id: "nav-channel-quotes", label: "Idź do katalogu ofert z kanału", to: "/channel-quotes" },
  { id: "nav-rate-lines", label: "Idź do stawek kupna", to: "/rate-lines" },
  { id: "nav-quotations", label: "Idź do wycen", to: "/quotations" },
  { id: "nav-organization-settings", label: "Idź do ustawień tenanta", to: "/organization-settings" },
  { id: "nav-session", label: "Ustawienia sesji (tenant)", to: "/session" },
] as const

export function commandPaletteActionIds(): string[] {
  return [...NAV_ACTIONS.map((action) => action.id), ...OPERATOR_ACTIONS.map((action) => action.id)]
}

const PALETTE_ITEM_CLASS = cn(
  "flex cursor-pointer items-center rounded-md px-2 py-1.5 text-sm text-foreground",
  "data-[selected=true]:bg-muted",
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
)

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
        <Command data-operator-target="command-palette" label="Paleta poleceń" shouldFilter>
          <div className="flex items-center gap-2 border-b border-border px-3">
            <Search className="size-4 text-muted-foreground" />
            <Command.Input
              value={query}
              onValueChange={setQuery}
              placeholder="Szukaj akcji…"
              className="h-10 w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring"
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
                  className={PALETTE_ITEM_CLASS}
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
                  className={PALETTE_ITEM_CLASS}
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
