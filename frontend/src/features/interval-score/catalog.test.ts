import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("interval_score surface for 443.0", () => {
  it("lists computed scores on /interval-scores without composer or Money", () => {
    const page = src("features/interval-score/catalog-page.tsx")
    expect(src("routes/interval-scores.tsx")).toContain("/interval-scores")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/interval-scores"')
    expect(src("lib/business-lists.ts")).toContain("intervalScore")
    expect(page).toContain('data-interval-score="desk"')
    expect(page).not.toContain("Composer")
    expect(page).not.toContain("createIntervalScore")
    expect(page).not.toContain("<Money")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("leaflet")
    expect(src("lib/interval-scores-api.ts")).not.toContain("method: \"POST\"")
    expect(src("features/ops/ops-index.ts")).toContain('"443.0": "/interval-scores"')
  })
})
