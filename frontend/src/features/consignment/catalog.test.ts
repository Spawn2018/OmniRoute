import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { parcelWrite } from "@/lib/consignments-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("parcelWrite", () => {
  it("trims consignment fields without parsing money", () => {
    expect(
      parcelWrite({
        shipmentToken: "  ship  ",
        parcelRef: "CN-1",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      shipment_id: "ship",
      consignment_ref: "CN-1",
      source_ref: "tenant:manual",
    })
  })
})

describe("consignment surface for 260.0", () => {
  it("records a przesylka on /consignments without FTL unique", () => {
    const page = src("features/consignment/catalog-page.tsx")
    const panel = src("features/consignment/parcel-panel.tsx")
    const ops = src("features/ops/ops-index.ts")
    expect(src("routes/consignments.tsx")).toMatch(/\/consignments/)
    expect(src("components/layout/sidebar.tsx")).toMatch(/to: "\/consignments"/)
    expect(src("lib/business-lists.ts")).toMatch(/consignment:/)
    expect(page).toMatch(/data-consignment="board"/)
    expect(page).toMatch(/ParcelMarkPanel/)
    expect(panel).toMatch(/persistParcel/)
    expect(panel).toMatch(/data-consignment="parcel-form"/)
    expect(panel).toMatch(/Zapisz przesyłkę/)
    expect(panel).toMatch(/ConsignmentMarks/)
    expect(/parseFloat|leaflet|CatalogCreateForm|buy_amount/.test(panel)).toBe(false)
    expect(ops).toMatch(/"260\.0": "\/consignments"/)
  })
})
