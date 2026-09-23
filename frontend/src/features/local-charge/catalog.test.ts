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
        portToken: " plgdy ",
        isoToken: " 22g1 ",
        carrierToken: " MSC ",
        serviceToken: " AE1 ",
      }),
    ).toEqual({
      charge_kind: "thc",
      amount: "80.0000",
      currency: "EUR",
      source_ref: "tenant:manual",
      port_unlocode: "PLGDY",
      iso_size_type: "22G1",
      carrier_label: "MSC",
      service_label: "AE1",
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
    expect(src("features/ops/ops-index.ts")).toContain('"207.0": "/local-charges"')
    expect(src("features/ops/ops-index.ts")).toContain('"208.0": "/local-charges"')
    expect(src("features/ops/ops-index.ts")).toContain('"633.0": "/local-charges"')
    expect(panel).toContain("Typ ISO kontenera")
    expect(panel).toContain("Armator")
    expect(panel).toContain("Serwis liniowy")
  })
})
