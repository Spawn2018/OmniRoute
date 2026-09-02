import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

function readFrontend(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

describe("sales invoice surface for 33.0", () => {
  it("ships /invoices as sell amounts from charge without KSeF", () => {
    const board = readFrontend("features/sales-invoice/catalog-page.tsx")
    expect(readFrontend("routes/invoices.tsx")).toContain("/invoices")
    expect(readFrontend("components/layout/sidebar.tsx")).toContain("/invoices")
    expect(readFrontend("lib/business-lists.ts")).toContain("salesInvoice")
    expect(readFrontend("features/ops/ops-index.ts")).toContain("/invoices")
    expect(board).toContain('data-sales-invoice="board"')
    expect(board).toContain("fetchCharges")
    expect(board).toContain("sell_amount")
    expect(board).not.toContain("ksef")
    expect(board).not.toContain("buy_amount -")
    expect(board).not.toContain("CatalogCreateForm")
  })
})
