import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { airPorts } from "@/lib/ports-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("airPorts", () => {
  it("keeps ports whose function_flags include airport", () => {
    expect(
      airPorts([
        { function_flags: ["port"] },
        { function_flags: ["port", "airport"] },
        { function_flags: ["rail"] },
      ]),
    ).toEqual([{ function_flags: ["port", "airport"] }])
  })
})

describe("air surface for 154.0", () => {
  it("records an air shipment_leg on /air without HAWB", () => {
    const page = src("features/air-freight/catalog-page.tsx")
    const panel = src("features/air-freight/airway-leg-panel.tsx")
    expect(src("routes/air.tsx")).toContain("/air")
    expect(src("components/layout/sidebar.tsx")).toContain("/air")
    expect(src("lib/business-lists.ts")).toContain("airFreight")
    expect(page).toContain('data-air="run"')
    expect(page).toContain("airPorts")
    expect(page).toContain("AirwayLegPanel")
    expect(panel).toContain('leg_kind: "air"')
    expect(panel).toContain('data-air="leg-form"')
    expect(panel).toContain("Zapisz odcinek lotniczy")
    expect(panel).toContain("hawb_no")
    expect(panel).toContain("mawb_no")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"154.0": "/air"')
    expect(src("features/ops/ops-index.ts")).toContain('"209.0": "/air"')
    expect(src("features/ops/ops-index.ts")).toContain('"619.0": "/air"')
    expect(src("features/ops/ops-index.ts")).toContain('"622.0": "/air"')
    expect(page).toContain('/channel-quotes')
    expect(page).toContain("e-rates")
  })

  it("issues HAWB/MAWB from M-03 prefix without IATA check digit", () => {
    const panel = src("features/air-freight/airway-leg-panel.tsx")
    const api = src("lib/shipment-legs-api.ts")
    expect(panel).toContain("Nadaj HAWB")
    expect(panel).toContain("Nadaj MAWB")
    expect(panel).toContain("issueHawbNumber")
    expect(panel).toContain("issueMawbNumber")
    expect(panel).not.toContain("checkDigit")
    expect(api).toContain("hawb-number")
    expect(api).toContain("mawb-number")
  })
})
