import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { makeAutonomyLevelPayload } from "@/lib/autonomy-levels-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("makeAutonomyLevelPayload", () => {
  it("trims level fields without money math", () => {
    expect(
      makeAutonomyLevelPayload({
        levelCode: " observer ",
        sourceRef: "tenant:manual",
      }),
    ).toEqual({
      level_code: "observer",
      source_ref: "tenant:manual",
    })
  })
})

describe("autonomy_level surface for 438.0", () => {
  it("records an open level on /autonomy-levels without Money", () => {
    const page = src("features/autonomy-level/catalog-page.tsx")
    const panel = src("features/autonomy-level/ledger-form.tsx")
    expect(src("routes/autonomy-levels.tsx")).toContain("/autonomy-levels")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/autonomy-levels"')
    expect(src("lib/business-lists.ts")).toContain("autonomyLevel")
    expect(page).toContain('data-autonomy-level="desk"')
    expect(page).toContain("AutonomyLevelComposer")
    expect(panel).toContain("createAutonomyLevel")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz poziom autonomii")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"438.0": "/autonomy-levels"')
  })
})
