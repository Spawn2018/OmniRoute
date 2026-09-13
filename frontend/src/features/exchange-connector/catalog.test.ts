import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { exchangeBoardWrite } from "@/lib/exchange-connectors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("exchangeBoardWrite", () => {
  it("trims HITL fields without money math or live board HTTP", () => {
    const written = exchangeBoardWrite({
      boardMark: " trans_eu_desk ",
      kindToken: " trans_eu ",
      originHint: "tenant:manual",
    })
    expect(written.connector_code).toBe("trans_eu_desk")
    expect(written.system_kind).toBe("trans_eu")
    expect(written.source_ref).toBe("tenant:manual")
  })
})

describe("exchange_connector surface for 271.0", () => {
  it("wires the Trans.eu fixture catalog without a public portal", () => {
    const page = src("features/exchange-connector/catalog-page.tsx")
    const panel = src("features/exchange-connector/exchange-connector-form.tsx")
    const client = src("lib/exchange-connectors-api.ts")
    expect(src("routes/exchange-connectors.tsx")).toMatch(/createFileRoute\("\/exchange-connectors"\)/)
    expect(src("components/layout/sidebar.tsx")).toMatch(/Konektor giełdy/)
    expect(src("lib/business-lists.ts")).toMatch(/exchangeConnector/)
    expect(page).toMatch(/data-exchange-connector="fixture-desk"/)
    expect(page).toMatch(/ExchangeConnectorDesk/)
    expect(page).toMatch(/DataTableShell/)
    expect(page).toMatch(/CatalogHeading/)
    expect(panel).toMatch(/persistExchangeConnector/)
    expect(panel).toMatch(/Zapisz konektor giełdy/)
    expect(panel.includes("<Money")).toBe(false)
    expect(panel.includes("parseFloat")).toBe(false)
    expect(panel.includes("httpx")).toBe(false)
    expect(panel.includes("CatalogCreateForm")).toBe(false)
    expect(panel.includes("Wystaw fracht")).toBe(false)
    expect(panel.includes("OAuth")).toBe(false)
    expect(src("features/ops/ops-index.ts")).toMatch(/"271\.0": "\/exchange-connectors"/)
    expect(src("features/ops/ops-index.ts")).toMatch(/"473\.0": "\/exchange-connectors"/)
    expect(panel).toMatch(/BOARD_KIND_OPTIONS/)
    expect(panel).toMatch(/<select/)
    expect(client.includes("client_secret")).toBe(false)
  })
})
