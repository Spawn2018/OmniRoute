import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { oceanLclPorts } from "@/lib/ports-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("oceanLclPorts", () => {
  it("keeps seaports and drops inland rows", () => {
    expect(
      oceanLclPorts([
        { is_seaport: false },
        { is_seaport: true },
      ]),
    ).toEqual([{ is_seaport: true }])
  })
})

describe("ocean lcl surface for 44.0", () => {
  it("ships /lcl as seaports without an LCL table", () => {
    const page = src("features/ocean-lcl/catalog-page.tsx")
    expect(src("routes/lcl.tsx")).toContain("/lcl")
    expect(src("components/layout/sidebar.tsx")).toContain("/lcl")
    expect(src("lib/business-lists.ts")).toContain("oceanLcl")
    expect(src("features/ops/ops-index.ts")).toContain("/lcl")
    expect(page).toContain('data-ocean-lcl="board"')
    expect(page).toContain("oceanLclPorts")
    expect(page).toContain("fetchPorts")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
  })
})

describe("ocean lcl surface for 111.0", () => {
  it("records an ocean_lcl shipment_leg on /lcl", () => {
    const page = src("features/ocean-lcl/catalog-page.tsx")
    const board = src("features/ocean-lcl/ocean-lcl-leg-board.tsx")
    expect(page).toContain("OceanLclLegBoard")
    expect(board).toContain("listShipmentLegs")
    expect(board).toContain("saveShipmentLeg")
    expect(board).toContain('data-ocean-lcl="leg-form"')
    expect(board).toContain("Zapisz odcinek drobnicy")
    expect(board).toContain('leg_kind: "ocean_lcl"')
    expect(board).not.toContain("parseFloat")
    expect(board).not.toContain("leaflet")
    expect(board).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"111.0": "/lcl"')
  })
})
