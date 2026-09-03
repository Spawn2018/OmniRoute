import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

function frontendFile(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

describe("money cost surface for 36.0 and 100.0", () => {
  it("ships /money-cost without multiplying amounts", () => {
    const page = frontendFile("features/money-cost/catalog-page.tsx")
    expect(frontendFile("routes/money-cost.tsx")).toContain("/money-cost")
    expect(frontendFile("components/layout/sidebar.tsx")).toContain("/money-cost")
    expect(frontendFile("lib/business-lists.ts")).toContain("moneyCost")
    expect(frontendFile("features/ops/ops-index.ts")).toContain("/money-cost")
    expect(page).toContain('data-money-cost="board"')
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toMatch(/\*\s*mid|mid\s*\*/)
  })

  it("records 100.0 as live money costs on /money-cost", () => {
    const page = frontendFile("features/money-cost/catalog-page.tsx")
    const api = frontendFile("lib/money-costs-api.ts")
    const ops = frontendFile("features/ops/ops-index.ts")
    expect(ops).toContain('"100.0": "/money-cost"')
    expect(api).toContain("recordMoneyCost")
    expect(page).toContain("fetchMoneyCosts")
    expect(page).toContain("Zapisz koszt")
    expect(page).not.toContain("fetchCharges")
    expect(page).not.toContain("buy_amount")
    expect(page).not.toContain("fetchNbpRates")
  })
})
