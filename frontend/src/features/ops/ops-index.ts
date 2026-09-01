import { BUSINESS_LISTS } from "@/lib/business-lists"

export const ADMIN_REF_SURFACES = [
  "sidebar-density",
  "table-toolbar",
  "command-actions",
] as const

export const OPS_JOBS = [
  { route: BUSINESS_LISTS.extractions.route, label: "Ekstrakcje HITL", job: "extract / accept" },
  { route: BUSINESS_LISTS.chargeCodes.route, label: "Kody opłat", job: "katalog charge_code" },
  {
    route: BUSINESS_LISTS.commodityCodes.route,
    label: "Kody towarowe",
    job: "katalog commodity_code",
  },
  {
    route: BUSINESS_LISTS.dangerousGoods.route,
    label: "Towary niebezpieczne",
    job: "katalog dangerous_good UN/IMDG",
  },
  {
    route: BUSINESS_LISTS.networks.route,
    label: "Sieci",
    job: "katalog network per tenant",
  },
  {
    route: BUSINESS_LISTS.nbpRates.route,
    label: "Kursy NBP",
    job: "katalog nbp_rate tabeli A",
  },
  { route: BUSINESS_LISTS.rateLines.route, label: "Stawki kupna", job: "rate_line + source_ref" },
  { route: BUSINESS_LISTS.charges.route, label: "Opłaty", job: "buy+sell / marża" },
  { route: BUSINESS_LISTS.quotations.route, label: "Wyceny", job: "SQL z bieżącego rate_line" },
  { route: BUSINESS_LISTS.organizationSettings.route, label: "Ustawienia", job: "config jako dane" },
  { route: BUSINESS_LISTS.ports.route, label: "Porty", job: "katalog UN/LOCODE + resolve" },
  {
    route: BUSINESS_LISTS.locations.route,
    label: "Lokalizacje",
    job: "strefy taryfowe + resolve kodu",
  },
  {
    route: BUSINESS_LISTS.terminals.route,
    label: "Terminale",
    job: "katalog ISPS + resolve",
  },
  {
    route: BUSINESS_LISTS.parties.route,
    label: "Kontrahenci",
    job: "katalog party + resolve tax_id / mail",
  },
  {
    route: BUSINESS_LISTS.partyScorecards.route,
    label: "Karty wyników",
    job: "snapshot party_scorecard",
  },
  {
    route: BUSINESS_LISTS.customerSops.route,
    label: "Procedury klienta",
    job: "katalog customer_sop + zatwierdzenie",
  },
  { route: BUSINESS_LISTS.users.route, label: "Użytkownicy", job: "tenant users" },
  { route: "/session", label: "Sesja", job: "token klienta" },
] as const

export const HELLO_DASHBOARD_MARKERS = ["Shell 0.5", "hello-dashboard", "kafelki"] as const

export const SHIPPED_CHARGE_ROUTES = {
  "1.0": "/charge-codes",
  "1.1": "/rate-lines",
  "1.2": "/charges",
  "2.0": "/quotations",
  "3.0": "/organization-settings",
  "4.0": "/ports",
  "4.1": "/locations",
  "4.2": "/terminals",
  "5.0": "/parties",
  "5.2": "/commodity-codes",
  "6.0": "/nbp-rates",
  "7.0": "/dangerous-goods",
  "8.0": "/parties",
  "9.0": "/networks",
  "10.0": "/party-scorecards",
  "11.0": "/customer-sops",
} as const

export const ROUTES_BREADTH_STANDING =
  "Nowe BC z jobem operatora = trasa w tym samym plasterze. Charge 1.0–1.2 już mają UI. To standing, nie 70 modułów."
