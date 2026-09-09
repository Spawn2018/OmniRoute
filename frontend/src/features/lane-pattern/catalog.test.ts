import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { patternWrite } from "@/lib/lane-patterns-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("patternWrite", () => {
  it("trims pattern fields without km or money math", () => {
    expect(
      patternWrite({
        startStamp: " plgdy ",
        endStamp: " deham ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      origin_unlocode: "plgdy",
      destination_unlocode: "deham",
      source_ref: "tenant:manual",
    })
  })
})

describe("lane_pattern surface for 185.0", () => {
  it("records a corridor pattern on /lane-patterns without km or amount", () => {
    const page = src("features/lane-pattern/catalog-page.tsx")
    const panel = src("features/lane-pattern/pattern-form.tsx")
    expect(src("routes/lane-patterns.tsx")).toContain("/lane-patterns")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/lane-patterns"')
    expect(src("lib/business-lists.ts")).toContain("lanePattern")
    expect(page).toContain('data-lane-pattern="desk"')
    expect(page).toContain("PatternPanel")
    expect(panel).toContain("persistPatternMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz wzorzec korytarza")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"185.0": "/lane-patterns"')
  })
})
