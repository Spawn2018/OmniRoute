import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

function frontendFile(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

describe("quote invoice settlement surface for 34.0", () => {
  it("ships /quote-invoices as quotation sell pairs without a settlement table", () => {
    const page = frontendFile("features/quote-invoice-settlement/catalog-page.tsx")
    expect(frontendFile("routes/quote-invoices.tsx")).toContain("/quote-invoices")
    expect(frontendFile("components/layout/sidebar.tsx")).toContain("/quote-invoices")
    expect(frontendFile("lib/business-lists.ts")).toContain("quoteInvoiceSettlement")
    expect(frontendFile("features/ops/ops-index.ts")).toContain("/quote-invoices")
    expect(page).toContain('data-quote-invoice-settlement="board"')
    expect(page).toContain("quotationInvoiceSettlements")
    expect(page).toContain("fetchCharges")
    expect(page).toContain("fetchQuotations")
    expect(page).toContain("sell_amount")
    expect(page).not.toContain("ksef")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toMatch(/amount\s*-/)
  })
})
