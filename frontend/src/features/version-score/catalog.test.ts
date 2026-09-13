import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("version_score surface for 444.0", () => {
  it("lists computed averages on /version-scores without composer or Money", () => {
    const page = src("features/version-score/catalog-page.tsx")
    expect(src("routes/version-scores.tsx")).toContain("/version-scores")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/version-scores"')
    expect(src("lib/business-lists.ts")).toContain("versionScore")
    expect(page).toContain('data-version-score="desk"')
    expect(page).not.toContain("Composer")
    expect(page).not.toContain("createVersionScore")
    expect(page).not.toContain("<Money")
    expect(page).not.toContain("parseFloat")
    expect(src("lib/version-scores-api.ts")).not.toContain("method: \"POST\"")
    expect(src("features/ops/ops-index.ts")).toContain('"444.0": "/version-scores"')
  })
})
