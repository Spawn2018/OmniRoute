export const BUSINESS_LISTS = {
  users: { route: "/tenancy/users", tableKey: "tenancy.users" },
  chargeCodes: { route: "/charge-codes", tableKey: "charge_codes" },
  commodityCodes: { route: "/commodity-codes", tableKey: "commodity_codes" },
  nbpRates: { route: "/nbp-rates", tableKey: "nbp_rates" },
  rateLines: { route: "/rate-lines", tableKey: "rate_lines" },
  charges: { route: "/charges", tableKey: "charges" },
  quotations: { route: "/quotations", tableKey: "quotations" },
  organizationSettings: { route: "/organization-settings", tableKey: "organization_settings" },
  extractions: { route: "/extractions", tableKey: "extraction.queue" },
  ports: { route: "/ports", tableKey: "ports" },
  locations: { route: "/locations", tableKey: "locations" },
  terminals: { route: "/terminals", tableKey: "terminals" },
  parties: { route: "/parties", tableKey: "parties" },
} as const

export const REQUIRED_BUSINESS_LIST_ROUTES = [
  "/tenancy/users",
  "/charge-codes",
  "/commodity-codes",
  "/nbp-rates",
  "/rate-lines",
  "/charges",
  "/quotations",
  "/organization-settings",
  "/extractions",
  "/ports",
  "/locations",
  "/terminals",
  "/parties",
] as const

export function businessListRoutes(): string[] {
  return Object.values(BUSINESS_LISTS).map((list) => list.route)
}

export function businessListTableKeys(): string[] {
  return Object.values(BUSINESS_LISTS).map((list) => list.tableKey)
}
