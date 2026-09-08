import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { laneWrite } from "@/lib/tender-lanes-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("laneWrite", () => {
  it("trims corridor fields without parsing money", () => {
    expect(
      laneWrite({
        lotStamp: " 11111111-1111-1111-1111-111111111111 ",
        originStamp: " plgdy ",
        destStamp: " deham ",
        originRef: "tenant:manual",
      }),
    ).toEqual({
      tender_lot_id: "11111111-1111-1111-1111-111111111111",
      origin_unlocode: "plgdy",
      destination_unlocode: "deham",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_lane surface for 171.0", () => {
  it("records UN/LOCODE pair on /tender-lanes without auto-award", () => {
    const page = src("features/tender-lane/catalog-page.tsx")
    const panel = src("features/tender-lane/lane-form.tsx")
    expect(src("routes/tender-lanes.tsx")).toContain("/tender-lanes")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-lanes"')
    expect(src("lib/business-lists.ts")).toContain("tenderLane")
    expect(page).toContain('data-tender-lane="desk"')
    expect(page).toContain("LanePanel")
    expect(panel).toContain("persistLaneMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz korytarz")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"171.0": "/tender-lanes"')
  })
})
