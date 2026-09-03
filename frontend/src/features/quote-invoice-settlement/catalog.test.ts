import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

function frontendFile(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

describe("quote invoice settlement surface for 34.0 and 98.0", () => {
  it("ships /quote-invoices without subtracting amounts", () => {
    const page = frontendFile("features/quote-invoice-settlement/catalog-page.tsx")
    expect(frontendFile("routes/quote-invoices.tsx")).toContain("/quote-invoices")
    expect(frontendFile("components/layout/sidebar.tsx")).toContain("/quote-invoices")
    expect(frontendFile("lib/business-lists.ts")).toContain("quoteInvoiceSettlement")
    expect(frontendFile("features/ops/ops-index.ts")).toContain("/quote-invoices")
    expect(page).toContain('data-quote-invoice-settlement="board"')
    expect(page).not.toContain("ksef")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toMatch(/amount\s*-/)
  })

  it("records 98.0 as live settlements on /quote-invoices", () => {
    const page = frontendFile("features/quote-invoice-settlement/catalog-page.tsx")
    const api = frontendFile("lib/quote-invoice-settlements-api.ts")
    const ops = frontendFile("features/ops/ops-index.ts")
    expect(ops).toContain('"98.0": "/quote-invoices"')
    expect(api).toContain("createQuoteInvoiceSettlement")
    expect(page).toContain("fetchQuoteInvoiceSettlements")
    expect(page).toContain("Zapisz rozliczenie")
    expect(page).not.toContain("fetchCharges")
    expect(page).not.toContain("sell_amount")
    expect(page).not.toContain("quotationInvoiceSettlements")
  })
})
