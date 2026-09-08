import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { indexWrite } from "@/lib/fuel-indexes-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("indexWrite", () => {
  it("trims index fields without parsing money", () => {
    expect(
      indexWrite({
        kindToken: " FSC ",
        dayStamp: "2026-03-01",
        pointMark: "1.2500",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      index_kind: "fsc",
      published_on: "2026-03-01",
      index_value: "1.2500",
      source_ref: "tenant:manual",
    })
  })
})

describe("fuel_index surface for 165.0", () => {
  it("records an FSC index on /fuel-indexes without charge conversion", () => {
    const page = src("features/fuel-index/catalog-page.tsx")
    const panel = src("features/fuel-index/index-form.tsx")
    expect(src("routes/fuel-indexes.tsx")).toContain("/fuel-indexes")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/fuel-indexes"')
    expect(src("lib/business-lists.ts")).toContain("fuelIndex")
    expect(page).toContain('data-fuel-index="desk"')
    expect(page).toContain("IndexMarkPanel")
    expect(panel).toContain("persistIndexMark")
    expect(panel).toContain("Zapisz indeks paliwowy")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"165.0": "/fuel-indexes"')
  })
})
