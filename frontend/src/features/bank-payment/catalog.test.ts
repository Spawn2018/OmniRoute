import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

function frontendFile(rel: string): string {
  return readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../..", rel), "utf8")
}

describe("bank payment surface for 35.0 and 99.0", () => {
  it("ships /payments without subtracting amounts", () => {
    const page = frontendFile("features/bank-payment/catalog-page.tsx")
    expect(frontendFile("routes/payments.tsx")).toContain("/payments")
    expect(frontendFile("components/layout/sidebar.tsx")).toContain("/payments")
    expect(frontendFile("lib/business-lists.ts")).toContain("bankPayment")
    expect(frontendFile("features/ops/ops-index.ts")).toContain("/payments")
    expect(page).toContain('data-bank-payment="board"')
    expect(page).not.toContain("sepa")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("createBankAccount")
  })

  it("records 99.0 as live payments on /payments", () => {
    const page = frontendFile("features/bank-payment/catalog-page.tsx")
    const api = frontendFile("lib/bank-payments-api.ts")
    const ops = frontendFile("features/ops/ops-index.ts")
    expect(ops).toContain('"99.0": "/payments"')
    expect(api).toContain("recordBankPayment")
    expect(page).toContain("fetchBankPayments")
    expect(page).toContain("Zapisz płatność")
    expect(page).not.toContain("fetchCharges")
    expect(page).not.toContain("sell_amount")
    expect(page).not.toContain("lookupIban")
    expect(page).not.toContain("fetchBankAccounts")
  })
})
