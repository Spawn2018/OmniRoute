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
