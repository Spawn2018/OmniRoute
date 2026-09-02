import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { railPorts } from "@/lib/ports-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("railPorts", () => {
  it("keeps ports whose function_flags include rail", () => {
    expect(
      railPorts([
        { function_flags: ["port"] },
        { function_flags: ["port", "rail"] },
        { function_flags: ["airport"] },
      ]),
    ).toEqual([{ function_flags: ["port", "rail"] }])
  })
})

describe("intermodal rail surface for 42.0", () => {
  it("ships /rail as ports with rail flag without a wagon table", () => {
    const page = src("features/intermodal-rail/catalog-page.tsx")
    expect(src("routes/rail.tsx")).toContain("/rail")
    expect(src("components/layout/sidebar.tsx")).toContain("/rail")
    expect(src("lib/business-lists.ts")).toContain("intermodalRail")
    expect(src("features/ops/ops-index.ts")).toContain("/rail")
    expect(page).toContain('data-intermodal-rail="board"')
    expect(page).toContain("railPorts")
    expect(page).toContain("fetchPorts")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
