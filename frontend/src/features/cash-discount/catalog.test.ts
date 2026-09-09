import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { skontoWrite } from "@/lib/cash-discounts-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("skontoWrite", () => {
  it("trims cash discount fields without money math", () => {
    expect(
      skontoWrite({
        invoiceStamp: " 11111111-1111-1111-1111-111111111111 ",
        kindStamp: " skonto ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      sales_invoice_id: "11111111-1111-1111-1111-111111111111",
      discount_kind: "skonto",
      source_ref: "tenant:manual",
    })
  })
})

describe("cash_discount surface for 189.0", () => {
  it("records a discount kind on /cash-discounts without amount", () => {
    const page = src("features/cash-discount/catalog-page.tsx")
    const panel = src("features/cash-discount/paper-form.tsx")
    expect(src("routes/cash-discounts.tsx")).toContain("/cash-discounts")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/cash-discounts"')
    expect(src("lib/business-lists.ts")).toContain("cashDiscount")
    expect(page).toContain('data-cash-discount="desk"')
    expect(page).toContain("SkontoPanel")
    expect(panel).toContain("persistSkontoMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz skonto")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"189.0": "/cash-discounts"')
  })
})
