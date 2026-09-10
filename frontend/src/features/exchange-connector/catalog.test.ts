import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { exchangeBoardWrite } from "@/lib/exchange-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("exchangeBoardWrite", () => {
  it("trims HITL fields without money math or live board HTTP", () => {
    expect(
      exchangeBoardWrite({
        boardMark: " trans_eu_desk ",
        kindToken: " trans_eu ",
        originHint: "tenant:manual",
      }),
    ).toEqual({
      connector_code: "trans_eu_desk",
      system_kind: "trans_eu",
      source_ref: "tenant:manual",
    })
  })
})

describe("exchange_connector surface for 271.0", () => {
  it("records HITL Trans.eu fixture on /exchange-connectors without portal SPA", () => {
    const page = src("features/exchange-connector/catalog-page.tsx")
    const panel = src("features/exchange-connector/exchange-connector-form.tsx")
    expect(src("routes/exchange-connectors.tsx")).toContain("/exchange-connectors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/exchange-connectors"')
    expect(src("lib/business-lists.ts")).toContain("exchangeConnector")
    expect(page).toContain('data-exchange-connector="fixture-desk"')
    expect(page).toContain("ExchangeConnectorDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistExchangeConnector")
    expect(panel).toContain("Zapisz konektor giełdy")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("httpx")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("Wystaw fracht")
    expect(panel).not.toContain("OAuth")
    expect(src("features/ops/ops-index.ts")).toContain('"271.0": "/exchange-connectors"')
    expect(src("lib/exchange-connectors-api.ts")).not.toContain("client_secret")
  })
})
