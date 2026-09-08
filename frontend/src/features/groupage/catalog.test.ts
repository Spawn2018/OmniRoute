import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { groupageLineWrite } from "@/lib/groupage-lines-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("groupageLineWrite", () => {
  it("pads cutoff to seconds and keeps integer transit days", () => {
    expect(
      groupageLineWrite({
        code: "wa_hub",
        originId: "a",
        destId: "b",
        cutoff: "16:00",
        days: "2",
        dows: [1, 5],
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      line_code: "wa_hub",
      origin_location_id: "a",
      destination_location_id: "b",
      cutoff_local: "16:00:00",
      transit_days: 2,
      operating_dows: [1, 5],
      source_ref: "tenant:manual",
    })
  })
})

describe("groupage surface for 155.0", () => {
  it("records a groupage_line on /groupage without WMS", () => {
    const page = src("features/groupage/catalog-page.tsx")
    const panel = src("features/groupage/line-panel.tsx")
    expect(src("routes/groupage.tsx")).toContain("/groupage")
    expect(src("components/layout/sidebar.tsx")).toContain("/groupage")
    expect(src("lib/business-lists.ts")).toContain("groupageLines")
    expect(page).toContain('data-groupage="run"')
    expect(page).toContain("roadLocations")
    expect(page).toContain("GroupageLinePanel")
    expect(panel).toContain("saveGroupageLine")
    expect(panel).toContain('data-groupage="line-form"')
    expect(panel).toContain("Zapisz linię drobnicy")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(panel).not.toContain("wms")
    expect(src("features/ops/ops-index.ts")).toContain('"155.0": "/groupage"')
  })
})
