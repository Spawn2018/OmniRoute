import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { bookkeepingLines } from "@/lib/charges-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("bookkeepingLines", () => {
  it("joins charge_code name onto buy and sell without netting", () => {
    expect(
      bookkeepingLines(
        [
          {
            id: "c1",
            charge_code: "OCEAN",
            buy_amount: "10.0000",
            buy_currency: "EUR",
            sell_amount: "12.0000",
            sell_currency: "EUR",
          },
        ],
        [{ code: "OCEAN", name: "Fracht morski" }],
      ),
    ).toEqual([
      {
        id: "c1",
        charge_code: "OCEAN",
        code_name: "Fracht morski",
        buy_amount: "10.0000",
        buy_currency: "EUR",
        sell_amount: "12.0000",
        sell_currency: "EUR",
      },
    ])
  })
})

describe("bookkeeping surface for 40.0 and 104.0", () => {
  it("ships /bookkeeping without subtracting amounts", () => {
    const page = src("features/bookkeeping/catalog-page.tsx")
    expect(src("routes/bookkeeping.tsx")).toContain("/bookkeeping")
    expect(src("components/layout/sidebar.tsx")).toContain("/bookkeeping")
    expect(src("lib/business-lists.ts")).toContain("bookkeeping")
    expect(src("features/ops/ops-index.ts")).toContain("/bookkeeping")
    expect(page).toContain('data-bookkeeping="board"')
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("margin_amount")
  })

  it("records 104.0 as live bookkeeping rows on /bookkeeping", () => {
    const page = src("features/bookkeeping/catalog-page.tsx")
    const api = src("lib/bookkeeping-api.ts")
    const ops = src("features/ops/ops-index.ts")
    expect(ops).toContain('"104.0": "/bookkeeping"')
    expect(api).toContain("recordBookkeeping")
    expect(page).toContain("fetchBookkeeping")
    expect(page).toContain("Zapisz dekret")
    expect(page).not.toContain("fetchCharges")
    expect(page).not.toContain("bookkeepingLines")
    expect(page).not.toContain("fetchChargeCodes")
  })
})
