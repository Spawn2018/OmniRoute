import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { cashFlowLegs } from "@/lib/charges-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("cashFlowLegs", () => {
  it("maps buy to outflow and sell to inflow without netting", () => {
    expect(
      cashFlowLegs([
        {
          id: "c1",
          charge_code: "OCEAN",
          buy_amount: "100.0000",
          buy_currency: "EUR",
          sell_amount: "130.0000",
          sell_currency: "EUR",
        },
      ]),
    ).toEqual([
      {
        id: "c1",
        charge_code: "OCEAN",
        outflow_amount: "100.0000",
        outflow_currency: "EUR",
        inflow_amount: "130.0000",
        inflow_currency: "EUR",
      },
    ])
  })
})

describe("cash flow surface for 38.0 and 102.0", () => {
  it("ships /cashflows without subtracting amounts", () => {
    const page = src("features/cash-flow/catalog-page.tsx")
    expect(src("routes/cashflows.tsx")).toContain("/cashflows")
    expect(src("components/layout/sidebar.tsx")).toContain("/cashflows")
    expect(src("lib/business-lists.ts")).toContain("cashFlow")
    expect(src("features/ops/ops-index.ts")).toContain("/cashflows")
    expect(page).toContain('data-cash-flow="board"')
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("margin_amount")
  })

  it("records 102.0 as live cash-flow rows on /cashflows", () => {
    const page = src("features/cash-flow/catalog-page.tsx")
    const api = src("lib/cash-flows-api.ts")
    const ops = src("features/ops/ops-index.ts")
    expect(ops).toContain('"102.0": "/cashflows"')
    expect(api).toContain("recordCashFlow")
    expect(page).toContain("fetchCashFlows")
    expect(page).toContain("Zapisz przepływ")
    expect(page).not.toContain("fetchCharges")
    expect(page).not.toContain("cashFlowLegs")
  })
})
