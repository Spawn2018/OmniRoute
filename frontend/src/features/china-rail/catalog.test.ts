import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { chinaRailPorts } from "@/lib/ports-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("chinaRailPorts", () => {
  it("keeps CN rail ports and drops other countries", () => {
    expect(
      chinaRailPorts([
        { country_code: "PL", function_flags: ["rail"] },
        { country_code: "CN", function_flags: ["rail"] },
        { country_code: "CN", function_flags: ["port"] },
      ]),
    ).toEqual([{ country_code: "CN", function_flags: ["rail"] }])
  })
})

describe("china rail surface for 43.0", () => {
  it("ships /china-rail as CN rail ports without a corridor table", () => {
    const page = src("features/china-rail/catalog-page.tsx")
    expect(src("routes/china-rail.tsx")).toContain("/china-rail")
    expect(src("components/layout/sidebar.tsx")).toContain("/china-rail")
    expect(src("lib/business-lists.ts")).toContain("chinaRail")
    expect(src("features/ops/ops-index.ts")).toContain("/china-rail")
    expect(page).toContain('data-china-rail="board"')
    expect(page).toContain("chinaRailPorts")
    expect(page).toContain("fetchPorts")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
  })
})
