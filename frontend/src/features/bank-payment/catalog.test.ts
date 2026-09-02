import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("bank payment surface for 35.0", () => {
  it("ships /payments as IBAN and sell without a payment table", () => {
    const page = src("features/bank-payment/catalog-page.tsx")
    expect(src("routes/payments.tsx")).toContain("/payments")
    expect(src("components/layout/sidebar.tsx")).toContain("/payments")
    expect(src("lib/business-lists.ts")).toContain("bankPayment")
    expect(src("features/ops/ops-index.ts")).toContain("/payments")
    expect(page).toContain('data-bank-payment="board"')
    expect(page).toContain("fetchBankAccounts")
    expect(page).toContain("lookupIban")
    expect(page).toContain("fetchCharges")
    expect(page).toContain("sell_amount")
    expect(page).not.toContain("sepa")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("createBankAccount")
  })
})
