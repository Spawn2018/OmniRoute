import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { capWrite } from "@/lib/tender-quotes-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("capWrite", () => {
  it("trims bid fields without parsing money", () => {
    expect(
      capWrite({
        quoteStamp: " 11111111-1111-1111-1111-111111111111 ",
        untilStamp: "2026-12-31",
        capCount: "3",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      quotation_id: "11111111-1111-1111-1111-111111111111",
      valid_until: "2026-12-31",
      order_limit: 3,
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_quote surface for 168.0", () => {
  it("records validity and order limit on /tender-quotes without auto-award", () => {
    const page = src("features/tender-quote/catalog-page.tsx")
    const panel = src("features/tender-quote/cap-form.tsx")
    expect(src("routes/tender-quotes.tsx")).toContain("/tender-quotes")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-quotes"')
    expect(src("lib/business-lists.ts")).toContain("tenderQuote")
    expect(page).toContain('data-tender-quote="desk"')
    expect(page).toContain("CapPanel")
    expect(panel).toContain("persistCapMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz ofertę przetargową")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"168.0": "/tender-quotes"')
  })
})
