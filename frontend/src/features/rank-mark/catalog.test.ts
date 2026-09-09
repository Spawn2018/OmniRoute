import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { rankWrite } from "@/lib/rank-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("rankWrite", () => {
  it("trims axis without money math or auto-award", () => {
    expect(rankWrite({ axis: " carbon ", origin: "tenant:manual" })).toEqual({
      rank_kind: "carbon",
      source_ref: "tenant:manual",
    })
  })
})

describe("rank_mark surface for 203.0", () => {
  it("records a HITL axis on /rank-marks without Money or auto-award", () => {
    const page = src("features/rank-mark/catalog-page.tsx")
    const bench = src("features/rank-mark/rank-workbench.tsx")
    expect(src("routes/rank-marks.tsx")).toContain("/rank-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/rank-marks"')
    expect(src("lib/business-lists.ts")).toContain("rankMark")
    expect(page).toContain('data-rank-mark="desk"')
    expect(page).toContain("RankWorkbench")
    expect(bench).toContain("persistRankMark")
    expect(bench).not.toContain("<Money")
    expect(bench).toContain("Zapisz oś rankingu")
    expect(bench).not.toContain("parseFloat")
    expect(bench).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"203.0": "/rank-marks"')
  })
})
