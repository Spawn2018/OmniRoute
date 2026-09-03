import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { customerSopsForParty } from "@/lib/customer-sops-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("customerSopsForParty", () => {
  it("keeps SOP rows for the selected party and none when empty", () => {
    const rows = [
      { party_id: "p1", code: "a" },
      { party_id: "p2", code: "b" },
    ]
    expect(customerSopsForParty(rows, "p1")).toEqual([{ party_id: "p1", code: "a" }])
    expect(customerSopsForParty(rows, "")).toEqual([])
  })
})

describe("cost to serve surface for 39.0 and 103.0", () => {
  it("ships /cost-to-serve without summing amounts", () => {
    const page = src("features/cost-to-serve/catalog-page.tsx")
    expect(src("routes/cost-to-serve.tsx")).toContain("/cost-to-serve")
    expect(src("components/layout/sidebar.tsx")).toContain("/cost-to-serve")
    expect(src("lib/business-lists.ts")).toContain("costToServe")
    expect(src("features/ops/ops-index.ts")).toContain("/cost-to-serve")
    expect(page).toContain('data-cost-to-serve="board"')
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("reduce(")
  })

  it("records 103.0 as live cost-to-serve rows on /cost-to-serve", () => {
    const page = src("features/cost-to-serve/catalog-page.tsx")
    const api = src("lib/cost-to-serve-api.ts")
    const ops = src("features/ops/ops-index.ts")
    expect(ops).toContain('"103.0": "/cost-to-serve"')
    expect(api).toContain("recordCostToServe")
    expect(page).toContain("fetchCostToServeRows")
    expect(page).toContain("Zapisz koszt obsługi")
    expect(page).not.toContain("fetchQuotations")
    expect(page).not.toContain("customerSopsForParty")
    expect(page).not.toContain("fetchParties")
  })
})
