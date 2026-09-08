import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { bandWrite } from "@/lib/groupage-tariffs-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("bandWrite", () => {
  it("trims tariff fields without parsing money", () => {
    expect(
      bandWrite({
        zoneToken: "  loc  ",
        bandToken: "band_west",
        massMark: "100.0000",
        cashMark: "85.5000",
        ccyMark: "eur",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      location_id: "loc",
      tariff_code: "band_west",
      chargeable_weight: "100.0000",
      amount: "85.5000",
      currency: "EUR",
      source_ref: "tenant:manual",
    })
  })
})

describe("groupage_tariff surface for 159.0", () => {
  it("records a weight band on /groupage-tariffs without matching engine", () => {
    const page = src("features/groupage-tariff/catalog-page.tsx")
    const panel = src("features/groupage-tariff/band-form.tsx")
    expect(src("routes/groupage-tariffs.tsx")).toContain("/groupage-tariffs")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/groupage-tariffs"')
    expect(src("lib/business-lists.ts")).toContain("groupageTariff")
    expect(page).toContain('data-tariff="desk"')
    expect(page).toContain("WeightBandPanel")
    expect(panel).toContain("persistWeightBand")
    expect(panel).toContain("<Money")
    expect(panel).toContain("Zapisz próg cennika drobnicy")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"159.0": "/groupage-tariffs"')
  })
})
