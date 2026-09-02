import { Link } from "@tanstack/react-router"
import { cn } from "@/lib/utils"

const NAV = [
  { to: "/", label: "Pulpit" },
  { to: "/tenancy/users", label: "Użytkownicy" },
  { to: "/extractions", label: "Ekstrakcje" },
  { to: "/finance", label: "Tablica finansowa" },
  { to: "/invoices", label: "Faktury" },
  { to: "/quote-invoices", label: "Rozliczenie wyceny" },
  { to: "/payments", label: "Bank i płatności" },
  { to: "/money-cost", label: "Koszt pieniądza" },
  { to: "/fx-differences", label: "Różnice kursowe" },
  { to: "/cashflows", label: "Przepływy" },
  { to: "/cost-to-serve", label: "Koszt obsługi klienta" },
  { to: "/bookkeeping", label: "Księgowość" },
  { to: "/road", label: "Transport drogowy" },
  { to: "/rail", label: "Kolej intermodalna" },
  { to: "/china-rail", label: "Kolej z Chin" },
  { to: "/lcl", label: "Drobnica morska" },
  { to: "/sanctions", label: "Sankcje" },
  { to: "/gdpr", label: "RODO" },
  { to: "/ai", label: "Propozycje AI" },
  { to: "/mail", label: "Poczta" },
  { to: "/notifications", label: "Powiadomienia" },
  { to: "/shipments", label: "Zlecenia" },
  { to: "/tracking", label: "Tracking" },
  { to: "/exceptions", label: "Wyjątki" },
  { to: "/shipment-documents", label: "Dokumenty zlecenia" },
  { to: "/edi", label: "EDI" },
  { to: "/charge-codes", label: "Kody opłat" },
  { to: "/commodity-codes", label: "Kody towarowe" },
  { to: "/dangerous-goods", label: "Towary niebezpieczne" },
  { to: "/networks", label: "Sieci" },
  { to: "/nbp-rates", label: "Kursy NBP" },
  { to: "/charges", label: "Opłaty" },
  { to: "/channel-quotes", label: "Oferty kanału" },
  { to: "/rate-lines", label: "Stawki" },
  { to: "/quotations", label: "Wyceny" },
  { to: "/ports", label: "Porty" },
  { to: "/port-surcharges", label: "Opłaty portowe" },
  { to: "/locations", label: "Lokalizacje" },
  { to: "/terminals", label: "Terminale" },
  { to: "/parties", label: "Kontrahenci" },
  { to: "/party-scorecards", label: "Karty wyników" },
  { to: "/customer-sops", label: "Procedury klienta" },
  { to: "/credit-reviews", label: "Recenzje kredytowe" },
  { to: "/organization-settings", label: "Ustawienia" },
  { to: "/session", label: "Sesja" },
] as const

export function Sidebar({ currentPath }: { currentPath: string }) {
  return (
    <aside
      data-admin-ref="sidebar-density"
      className="flex w-44 shrink-0 flex-col border-r border-border bg-sidebar text-sidebar-foreground"
    >
      <div className="border-b border-border px-2 py-1.5">
        <div className="text-sm font-semibold tracking-tight">OmniRoute</div>
        <div className="text-[11px] text-muted-foreground">gęsty admin</div>
      </div>
      <nav className="flex flex-col gap-px p-1">
        {NAV.map((item) => {
          const active = currentPath === item.to
          return (
            <Link
              key={item.to}
              to={item.to}
              aria-current={active ? "page" : undefined}
              className={cn(
                "rounded-md px-2 py-1 text-xs hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                active && "bg-muted font-medium",
              )}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto border-t border-border px-2 py-1.5 text-[11px] text-muted-foreground">
        ⌘K · akcje operatora
      </div>
    </aside>
  )
}
