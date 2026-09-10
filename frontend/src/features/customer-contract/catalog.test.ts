import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { pactHeaderWrite } from "@/lib/customer-contracts-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("pactHeaderWrite", () => {
  it("trims HITL header fields without money math or PDF unwrap", () => {
    const written = pactHeaderWrite({
      pactMark: " acme_pl_2026 ",
      loaderHint: " Acme Logistics ",
      buyerHint: " Bayer PL ",
      originHint: "tenant:manual",
    })
    expect(written.contract_code).toBe("acme_pl_2026")
    expect(written.shipper_label).toBe("Acme Logistics")
    expect(written.their_customer_label).toBe("Bayer PL")
    expect(written.source_ref).toBe("tenant:manual")
  })
})

describe("customer_contract surface for 272.0", () => {
  it("wires the header catalog without a PDF viewer or unwrap", () => {
    const page = src("features/customer-contract/catalog-page.tsx")
    const panel = src("features/customer-contract/header-form.tsx")
    const client = src("lib/customer-contracts-api.ts")
    expect(src("routes/customer-contracts.tsx")).toMatch(/createFileRoute\("\/customer-contracts"\)/)
    expect(src("components/layout/sidebar.tsx")).toMatch(/Umowa klienta/)
    expect(src("lib/business-lists.ts")).toMatch(/customerContract/)
    expect(page).toMatch(/data-customer-contract="header-desk"/)
    expect(page).toMatch(/CustomerContractDesk/)
    expect(page).toMatch(/DataTableShell/)
    expect(page).toMatch(/CatalogHeading/)
    expect(panel).toMatch(/persistCustomerContract/)
    expect(panel).toMatch(/Zapisz nagłówek umowy/)
    expect(panel.includes("<Money")).toBe(false)
    expect(panel.includes("parseFloat")).toBe(false)
    expect(panel.includes("unwrap")).toBe(false)
    expect(panel.includes("PDF")).toBe(false)
    expect(src("features/ops/ops-index.ts")).toMatch(/"272\.0": "\/customer-contracts"/)
    expect(client.includes("blob_ciphertext")).toBe(false)
    expect(client.includes("wrapped_dek")).toBe(false)
  })
})
