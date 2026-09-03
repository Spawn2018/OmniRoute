import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"
import { nbpRatesForKnownCurrencies, type NbpRate } from "@/lib/nbp-rates-api"

function frontendFile(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

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

describe("fx difference surface for 37.0 and 101.0", () => {
  it("ships /fx-differences without converting amounts", () => {
    const page = frontendFile("features/fx-difference/catalog-page.tsx")
    expect(frontendFile("routes/fx-differences.tsx")).toContain("/fx-differences")
    expect(frontendFile("components/layout/sidebar.tsx")).toContain("/fx-differences")
    expect(frontendFile("lib/business-lists.ts")).toContain("fxDifference")
    expect(frontendFile("features/ops/ops-index.ts")).toContain("/fx-differences")
    expect(page).toContain('data-fx-difference="board"')
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toMatch(/\*\s*mid|mid\s*\*/)
  })

  it("records 101.0 as live fx rows on /fx-differences", () => {
    const page = frontendFile("features/fx-difference/catalog-page.tsx")
    const api = frontendFile("lib/fx-differences-api.ts")
    const ops = frontendFile("features/ops/ops-index.ts")
    expect(ops).toContain('"101.0": "/fx-differences"')
    expect(api).toContain("recordFxDifference")
    expect(page).toContain("fetchFxDifferences")
    expect(page).toContain("Zapisz różnicę")
    expect(page).not.toContain("fetchCharges")
    expect(page).not.toContain("nbpRatesForKnownCurrencies")
    expect(page).not.toContain("fetchNbpRates")
  })
})
