export const BUSINESS_LISTS = {
  users: { route: "/tenancy/users", tableKey: "tenancy.users" },
  chargeCodes: { route: "/charge-codes", tableKey: "charge_codes" },
  commodityCodes: { route: "/commodity-codes", tableKey: "commodity_codes" },
  dangerousGoods: { route: "/dangerous-goods", tableKey: "dangerous_goods" },
  networks: { route: "/networks", tableKey: "networks" },
  nbpRates: { route: "/nbp-rates", tableKey: "nbp_rates" },
  rateLines: { route: "/rate-lines", tableKey: "rate_lines" },
  charges: { route: "/charges", tableKey: "charges" },
  quotations: { route: "/quotations", tableKey: "quotations" },
  organizationSettings: { route: "/organization-settings", tableKey: "organization_settings" },
  extractions: { route: "/extractions", tableKey: "extraction.queue" },
  ports: { route: "/ports", tableKey: "ports" },
  portSurcharges: { route: "/port-surcharges", tableKey: "port_surcharges" },
  locations: { route: "/locations", tableKey: "locations" },
  terminals: { route: "/terminals", tableKey: "terminals" },
  parties: { route: "/parties", tableKey: "parties" },
  partyScorecards: { route: "/party-scorecards", tableKey: "party_scorecards" },
  customerSops: { route: "/customer-sops", tableKey: "customer_sops" },
} as const

export const REQUIRED_BUSINESS_LIST_ROUTES = [
  "/tenancy/users",
  "/charge-codes",
  "/commodity-codes",
  "/dangerous-goods",
  "/networks",
  "/nbp-rates",
  "/rate-lines",
  "/charges",
  "/quotations",
  "/organization-settings",
  "/extractions",
  "/ports",
  "/port-surcharges",
  "/locations",
  "/terminals",
  "/parties",
  "/party-scorecards",
  "/customer-sops",
] as const

export function businessListRoutes(): string[] {
  return Object.values(BUSINESS_LISTS).map((list) => list.route)
}

export function businessListTableKeys(): string[] {
  return Object.values(BUSINESS_LISTS).map((list) => list.tableKey)
}
