import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { whenWrite } from "@/lib/rate-cards-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("whenWrite", () => {
  it("trims card fields without parsing money", () => {
    expect(
      whenWrite({
        codeToken: " weekend ",
        whenToken: " sobota ",
        cashMark: "10.5000",
        ccyMark: "eur",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      card_code: "weekend",
      applies_when: "sobota",
      amount: "10.5000",
      currency: "EUR",
      source_ref: "tenant:manual",
    })
  })
})

describe("rate_card surface for 163.0", () => {
    it("records an applies_when token on /rate-cards and matches equality in SQL", () => {
    const page = src("features/rate-card/catalog-page.tsx")
    const panel = src("features/rate-card/when-form.tsx")
    expect(src("routes/rate-cards.tsx")).toContain("/rate-cards")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/rate-cards"')
    expect(src("lib/business-lists.ts")).toContain("rateCard")
    expect(page).toContain('data-rate-card="desk"')
    expect(page).toContain("WhenTokenPanel")
    expect(panel).toContain("persistWhenMark")
    expect(panel).toContain("<Money")
    expect(panel).toContain("Zapisz kartę stawek")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"163.0": "/rate-cards"')
    expect(src("features/ops/ops-index.ts")).toContain('"205.0": "/rate-cards"')
    expect(page).toContain("WhenEqualStrip")
    expect(src("features/rate-card/when-equal.tsx")).toContain("Dopasuj warunek")
    expect(src("features/rate-card/when-equal.tsx")).not.toContain("parseFloat")
    expect(src("features/rate-card/when-equal.tsx")).not.toContain("<Money")
  })
})
