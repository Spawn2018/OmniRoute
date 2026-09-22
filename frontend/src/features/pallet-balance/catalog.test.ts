import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { poolWrite } from "@/lib/pallet-balances-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("poolWrite", () => {
  it("trims pallet count as integer without parseFloat", () => {
    expect(
      poolWrite({
        counterpartToken: "  party  ",
        kindToken: "lpr",
        countToken: "12",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      party_id: "party",
      pallet_kind: "lpr",
      unit_count: 12,
      source_ref: "tenant:manual",
    })
  })
})

describe("pallet_balance surface for 161.0", () => {
  it("records a Chep/LPR count on /pallet-balances without money", () => {
    const page = src("features/pallet-balance/catalog-page.tsx")
    const panel = src("features/pallet-balance/pool-panel.tsx")
    expect(src("routes/pallet-balances.tsx")).toContain("/pallet-balances")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/pallet-balances"')
    expect(src("lib/business-lists.ts")).toContain("palletBalance")
    expect(page).toContain('data-pallet-balance="board"')
    expect(page).toContain("PoolKindPanel")
    expect(panel).toContain("persistPoolMark")
    expect(panel).toContain('data-pallet-balance="pool-form"')
    expect(panel).toContain("Zapisz saldo palet")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("buy_amount")
    expect(src("features/ops/ops-index.ts")).toContain('"161.0": "/pallet-balances"')
    expect(src("features/ops/ops-index.ts")).toContain('"623.0": "/pallet-balances"')
    expect(panel).toContain("epal")
  })
})
