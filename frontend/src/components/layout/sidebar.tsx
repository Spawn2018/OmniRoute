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
  { to: "/ocean-bills", label: "Konosament LCL" },
  { to: "/air", label: "Lotniczy" },
  { to: "/groupage", label: "Linie drobnicy" },
  { to: "/groupage-tariffs", label: "Cennik drobnicy" },
  { to: "/shipment-packages", label: "Paczki" },
  { to: "/dock-appointments", label: "Awizacje doku" },
  { to: "/cod", label: "Pobranie COD" },
  { to: "/sanctions", label: "Sankcje" },
  { to: "/fraud", label: "Oszustwo" },
  { to: "/gdpr", label: "RODO" },
  { to: "/ai", label: "Propozycje AI" },
  { to: "/health", label: "Obserwowalność" },
  { to: "/quality", label: "Jakość ekstrakcji" },
  { to: "/rollout", label: "Wdrożenie" },
  { to: "/mail", label: "Poczta" },
  { to: "/notifications", label: "Powiadomienia" },
  { to: "/outbox", label: "Outbox" },
  { to: "/entity-events", label: "Zdarzenia podmiotu" },
  { to: "/shipments", label: "Zlecenia" },
  { to: "/tracking", label: "Tracking" },
  { to: "/exceptions", label: "Wyjątki" },
  { to: "/claims", label: "Reklamacje ładunku" },
  { to: "/watchtower", label: "Wieża" },
  { to: "/shipment-documents", label: "Dokumenty zlecenia" },
  { to: "/edi", label: "EDI" },
  { to: "/charge-codes", label: "Kody opłat" },
  { to: "/charge-templates", label: "Szablony opłat" },
  { to: "/commodity-codes", label: "Kody towarowe" },
  { to: "/dangerous-goods", label: "Towary niebezpieczne" },
  { to: "/networks", label: "Sieci" },
  { to: "/nbp-rates", label: "Kursy NBP" },
  { to: "/fuel-indexes", label: "Indeksy paliwowe" },
  { to: "/charges", label: "Opłaty" },
  { to: "/channel-quotes", label: "Oferty kanału" },
  { to: "/rate-lines", label: "Stawki" },
  { to: "/rate-cards", label: "Karty stawek" },
  { to: "/quotations", label: "Wyceny" },
  { to: "/ports", label: "Porty" },
  { to: "/port-surcharges", label: "Opłaty portowe" },
  { to: "/local-charges", label: "Dopłaty lokalne" },
  { to: "/tender-data-rooms", label: "Pokoje danych" },
  { to: "/tender-matrix-cells", label: "Komórki matrycy" },
  { to: "/tender-playbooks", label: "Playbook przetargu" },
  { to: "/tender-win-losses", label: "Wynik przetargu" },
  { to: "/tender-consortium-members", label: "Konsorcjum przetargu" },
  { to: "/tender-rfp-intakes", label: "Przyjęcie RFP" },
  { to: "/tender-prospects", label: "Prospekt przetargu" },
  { to: "/tender-bid-stances", label: "Udział w przetargu" },
  { to: "/tender-carbon-marks", label: "Ślad węglowy przetargu" },
  { to: "/lane-patterns", label: "Wzorzec korytarza" },
  { to: "/kreptd-licences", label: "Licencja KREPTD" },
  { to: "/monitoring-schemes", label: "Schemat monitoringu" },
  { to: "/party-documents", label: "Dokument kontrahenta" },
  { to: "/cash-discounts", label: "Skonto" },
  { to: "/carbon-methods", label: "Metodyka CO₂" },
  { to: "/prediction-ledgers", label: "Ledger predykcji" },
  { to: "/weather-observations", label: "Pogoda" },
  { to: "/tender-award-reviews", label: "Cztery oczy nagrody" },
  { to: "/tender-ted-notices", label: "Ogłoszenie TED" },
  { to: "/tender-lanes", label: "Korytarze przetargu" },
  { to: "/tender-lots", label: "Partie przetargu" },
  { to: "/tender-rounds", label: "Rundy przetargu" },
  { to: "/tender-quotes", label: "Oferty przetargowe" },
  { to: "/tenders", label: "Przetargi" },
  { to: "/locations", label: "Lokalizacje" },
  { to: "/terminals", label: "Terminale" },
  { to: "/parties", label: "Kontrahenci" },
  { to: "/pallet-balances", label: "Saldo palet" },
  { to: "/document-templates", label: "Szablony wydruku" },
  { to: "/party-scorecards", label: "Karty wyników" },
  { to: "/customer-sops", label: "Procedury klienta" },
  { to: "/credit-reviews", label: "Recenzje kredytowe" },
  { to: "/decisions", label: "Decyzje" },
  { to: "/organization-settings", label: "Ustawienia" },
  { to: "/session", label: "Sesja" },
] as const

export function Sidebar({ currentPath }: { currentPath: string }) {
  return (
    <aside
      data-admin-ref="sidebar-density"
      className="flex h-full min-h-0 w-44 shrink-0 flex-col overflow-y-auto border-r border-border bg-sidebar text-sidebar-foreground"
    >
      <div className="border-b border-border px-2 py-1.5">
        <div className="text-sm font-semibold tracking-tight">OmniRoute</div>
        <div className="text-[11px] text-sidebar-foreground/70">gęsty admin</div>
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
                "rounded-sm px-2 py-1 text-xs text-sidebar-foreground/80 hover:bg-sidebar-foreground/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                active && "bg-sidebar-foreground/15 font-medium text-sidebar-foreground",
              )}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto border-t border-border px-2 py-1.5 text-[11px] text-sidebar-foreground/70">
        ⌘K · akcje operatora
      </div>
    </aside>
  )
}
