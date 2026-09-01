export const BUSINESS_LISTS = {
  users: { route: "/tenancy/users", tableKey: "tenancy.users" },
  chargeCodes: { route: "/charge-codes", tableKey: "charge_codes" },
  rateLines: { route: "/rate-lines", tableKey: "rate_lines" },
  charges: { route: "/charges", tableKey: "charges" },
  quotations: { route: "/quotations", tableKey: "quotations" },
  organizationSettings: { route: "/organization-settings", tableKey: "organization_settings" },
  extractions: { route: "/extractions", tableKey: "extraction.queue" },
  ports: { route: "/ports", tableKey: "ports" },
  locations: { route: "/locations", tableKey: "locations" },
} as const

export const REQUIRED_BUSINESS_LIST_ROUTES = [
  "/tenancy/users",
  "/charge-codes",
  "/rate-lines",
  "/charges",
  "/quotations",
  "/organization-settings",
  "/extractions",
  "/ports",
  "/locations",
] as const

export function businessListRoutes(): string[] {
  return Object.values(BUSINESS_LISTS).map((list) => list.route)
}

export function businessListTableKeys(): string[] {
  return Object.values(BUSINESS_LISTS).map((list) => list.tableKey)
}
