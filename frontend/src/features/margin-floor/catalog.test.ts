import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeMarginFloorPayload } from "@/lib/margin-floors-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeMarginFloorPayload", () => {
  it("trims floor fields without money math", () => {
    expect(
      makeMarginFloorPayload({
        floorCode: " floor_gdn_ham ",
        originUnlocode: " plgdn ",
        destinationUnlocode: " deham ",
        floorAmount: " 120 ",
        floorCurrency: " eur ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      floor_code: "floor_gdn_ham",
      origin_unlocode: "PLGDN",
      destination_unlocode: "DEHAM",
      floor_amount: "120",
      floor_currency: "EUR",
      source_ref: "tenant:manual",
    })
  })
})

describe("margin_floor surface for 527.0", () => {
  it("records a floor on /margin-floors with Money", () => {
    const page = src("features/margin-floor/catalog-page.tsx")
    const panel = src("features/margin-floor/floor-form.tsx")
    expect(src("routes/margin-floors.tsx")).toContain("/margin-floors")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/margin-floors"')
    expect(src("lib/business-lists.ts")).toContain("marginFloor")
    expect(page).toContain('data-margin-floor="desk"')
    expect(page).toContain("MarginFloorComposer")
    expect(page).toContain("<Money")
    expect(panel).toContain("createMarginFloor")
    expect(panel).toContain("Zapisz podłogę marży")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"527.0": "/margin-floors"')
    expect(src("features/ops/ops-index.ts")).toContain('"539.0": "/charges"')
  })
})
