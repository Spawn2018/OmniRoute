import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { nbpRatesForKnownCurrencies, type NbpRate } from "@/lib/nbp-rates-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

const rate = (currency: string): NbpRate => ({
  id: currency,
  organization_id: "org",
  currency,
  rate_date: "2026-09-01",
  mid: "4.0000",
  source_ref: "nbp:a",
})

describe("nbpRatesForKnownCurrencies", () => {
  it("keeps NBP rows whose currency appears on charge or quotation", () => {
    expect(
      nbpRatesForKnownCurrencies(
        [rate("EUR"), rate("USD"), rate("GBP")],
        [{ buy_currency: "EUR", sell_currency: "EUR" }],
        [{ currency: "USD" }],
      ),
    ).toEqual([rate("EUR"), rate("USD")])
  })
})

describe("fx difference surface for 37.0", () => {
  it("ships /fx-differences as NBP filtered to known currencies", () => {
    const page = src("features/fx-difference/catalog-page.tsx")
    expect(src("routes/fx-differences.tsx")).toContain("/fx-differences")
    expect(src("components/layout/sidebar.tsx")).toContain("/fx-differences")
    expect(src("lib/business-lists.ts")).toContain("fxDifference")
    expect(src("features/ops/ops-index.ts")).toContain("/fx-differences")
    expect(page).toContain('data-fx-difference="board"')
    expect(page).toContain("nbpRatesForKnownCurrencies")
    expect(page).toContain("fetchNbpRates")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toMatch(/\*\s*mid|mid\s*\*/)
  })
})
