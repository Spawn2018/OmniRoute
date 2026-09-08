import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { levyWrite } from "@/lib/local-charges-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("levyWrite", () => {
  it("trims levy fields without parsing money", () => {
    expect(
      levyWrite({
        kindToken: " THC ",
        cashMark: "80.0000",
        ccyMark: "eur",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      charge_kind: "thc",
      amount: "80.0000",
      currency: "EUR",
      source_ref: "tenant:manual",
    })
  })
})

describe("local_charge surface for 166.0", () => {
  it("records a THC levy on /local-charges without missing-surcharge warning", () => {
    const page = src("features/local-charge/catalog-page.tsx")
    const panel = src("features/local-charge/levy-form.tsx")
    expect(src("routes/local-charges.tsx")).toContain("/local-charges")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/local-charges"')
    expect(src("lib/business-lists.ts")).toContain("localCharge")
    expect(page).toContain('data-local-charge="desk"')
    expect(page).toContain("LevyKindPanel")
    expect(panel).toContain("persistLevyMark")
    expect(panel).toContain("<Money")
    expect(panel).toContain("Zapisz dopłatę lokalną")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"166.0": "/local-charges"')
  })
})
