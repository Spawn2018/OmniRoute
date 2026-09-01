import { BUSINESS_LISTS } from "@/lib/business-lists"

export const ADMIN_REF_SURFACES = [
  "sidebar-density",
  "table-toolbar",
  "command-actions",
] as const

export const OPS_JOBS = [
  { route: BUSINESS_LISTS.extractions.route, label: "Ekstrakcje HITL", job: "extract / accept" },
  { route: BUSINESS_LISTS.chargeCodes.route, label: "Kody opłat", job: "katalog charge_code" },
  { route: BUSINESS_LISTS.rateLines.route, label: "Stawki kupna", job: "rate_line + source_ref" },
  { route: BUSINESS_LISTS.charges.route, label: "Opłaty", job: "buy+sell / marża" },
  { route: BUSINESS_LISTS.users.route, label: "Użytkownicy", job: "tenant users" },
  { route: "/session", label: "Sesja", job: "token klienta" },
] as const

export const HELLO_DASHBOARD_MARKERS = ["Shell 0.5", "hello-dashboard", "kafelki"] as const

export const SHIPPED_CHARGE_ROUTES = {
  "1.0": "/charge-codes",
  "1.1": "/rate-lines",
  "1.2": "/charges",
} as const

export const ROUTES_BREADTH_STANDING =
  "Nowe BC z jobem operatora = trasa w tym samym plasterze. Charge 1.0–1.2 już mają UI. To standing, nie 70 modułów."
