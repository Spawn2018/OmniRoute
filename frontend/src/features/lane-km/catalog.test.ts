import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { laneKmWrite } from "@/lib/lane-kms-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("laneKmWrite", () => {
  it("trims HITL fields without money math or Haversine", () => {
    expect(
      laneKmWrite({
        codeStamp: " backhaul_a ",
        loadedStamp: " 120.5 ",
        emptyStamp: " 40 ",
        approachStamp: " 15.25 ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      km_code: "backhaul_a",
      loaded_km: "120.5",
      empty_km: "40",
      approach_km: "15.25",
      source_ref: "tenant:manual",
    })
  })
})

describe("lane_km surface for 267.0", () => {
  it("records HITL km on /lane-kms without Money or map", () => {
    const page = src("features/lane-km/catalog-page.tsx")
    const panel = src("features/lane-km/lane-km-form.tsx")
    expect(src("routes/lane-kms.tsx")).toContain("/lane-kms")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/lane-kms"')
    expect(src("lib/business-lists.ts")).toContain("laneKm")
    expect(page).toContain('data-lane-km="desk"')
    expect(page).toContain("LaneKmDesk")
    expect(page).toContain("DataTableShell")
    expect(page).toContain("CatalogHeading")
    expect(panel).toContain("persistLaneKm")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz km korytarza")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"267.0": "/lane-kms"')
  })
})
