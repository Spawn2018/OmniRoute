import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

function readFrontend(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

describe("sales invoice surface for 33.0, 96.0 and 97.0", () => {
  it("ships /invoices without subtracting buy from sell", () => {
    const page = readFrontend("features/sales-invoice/catalog-page.tsx")
    expect(readFrontend("routes/invoices.tsx")).toContain("/invoices")
    expect(readFrontend("components/layout/sidebar.tsx")).toContain("/invoices")
    expect(readFrontend("lib/business-lists.ts")).toContain("salesInvoice")
    expect(readFrontend("features/ops/ops-index.ts")).toContain("/invoices")
    expect(page).toContain('data-sales-invoice="board"')
    expect(page).not.toContain("buy_amount -")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("xml")
    expect(page).not.toContain("fa3")
  })

  it("records 96.0 as live sales invoices on /invoices", () => {
    const page = readFrontend("features/sales-invoice/catalog-page.tsx")
    const api = readFrontend("lib/sales-invoices-api.ts")
    const ops = readFrontend("features/ops/ops-index.ts")
    expect(ops).toContain('"96.0": "/invoices"')
    expect(api).toContain("createSalesInvoice")
    expect(page).toContain("fetchSalesInvoices")
    expect(page).toContain("Zapisz fakturę")
    expect(page).not.toContain("fetchCharges")
    expect(page).not.toContain("sell_amount")
  })

  it("records 97.0 ksef session on the same /invoices board", () => {
    const page = readFrontend("features/sales-invoice/catalog-page.tsx")
    const api = readFrontend("lib/sales-invoices-api.ts")
    const ops = readFrontend("features/ops/ops-index.ts")
    expect(ops).toContain('"97.0": "/invoices"')
    expect(api).toContain("noteKsef")
    expect(page).toContain("ksef_ref")
    expect(page).toContain("Zapisz numer sesji")
    expect(page).not.toContain("xml")
    expect(page).not.toContain("fa3")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
