import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("money cost surface for 36.0", () => {
  it("ships /money-cost as NBP and buy without multiplying", () => {
    const page = src("features/money-cost/catalog-page.tsx")
    expect(src("routes/money-cost.tsx")).toContain("/money-cost")
    expect(src("components/layout/sidebar.tsx")).toContain("/money-cost")
    expect(src("lib/business-lists.ts")).toContain("moneyCost")
    expect(src("features/ops/ops-index.ts")).toContain("/money-cost")
    expect(page).toContain('data-money-cost="board"')
    expect(page).toContain("fetchNbpRates")
    expect(page).toContain("fetchCharges")
    expect(page).toContain("buy_amount")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toMatch(/\*\s*mid|mid\s*\*/)
  })
})
