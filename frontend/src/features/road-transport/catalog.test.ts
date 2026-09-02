import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { roadLocations } from "@/lib/locations-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("roadLocations", () => {
  it("keeps postal_zone and address and drops unlocode", () => {
    expect(
      roadLocations([
        { kind: "unlocode" },
        { kind: "postal_zone" },
        { kind: "address" },
      ]),
    ).toEqual([{ kind: "postal_zone" }, { kind: "address" }])
  })
})

describe("road transport surface for 41.0", () => {
  it("ships /road as land locations without TMS", () => {
    const page = src("features/road-transport/catalog-page.tsx")
    expect(src("routes/road.tsx")).toContain("/road")
    expect(src("components/layout/sidebar.tsx")).toContain("/road")
    expect(src("lib/business-lists.ts")).toContain("roadTransport")
    expect(src("features/ops/ops-index.ts")).toContain("/road")
    expect(page).toContain('data-road-transport="board"')
    expect(page).toContain("roadLocations")
    expect(page).toContain("fetchLocations")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("unlocode")
  })
})
