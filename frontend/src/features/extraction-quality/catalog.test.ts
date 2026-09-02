import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { qualityGaps } from "@/lib/extractions-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("qualityGaps", () => {
  it("keeps drafts with unparsed regions and drops empty", () => {
    expect(
      qualityGaps([
        { payload: { unparsed_regions: [] } },
        { payload: { unparsed_regions: ["footer"] } },
      ]),
    ).toEqual([{ payload: { unparsed_regions: ["footer"] } }])
  })
})

describe("extraction quality surface for 49.0", () => {
  it("ships /quality as unparsed regions without a scoring table", () => {
    const page = src("features/extraction-quality/catalog-page.tsx")
    expect(src("routes/quality.tsx")).toContain("/quality")
    expect(src("components/layout/sidebar.tsx")).toContain("/quality")
    expect(src("lib/business-lists.ts")).toContain("extractionQuality")
    expect(src("features/ops/ops-index.ts")).toContain("/quality")
    expect(page).toContain('data-extraction-quality="board"')
    expect(page).toContain('t("extraction_quality.title")')
    expect(page).not.toContain("Jakość ekstrakcji")
    expect(page).toContain("qualityGaps")
    expect(page).toContain("fetchExtractionDrafts")
    expect(page).toContain("unparsed_regions")
    expect(page).not.toContain("input_text")
    expect(page).not.toContain("ab_delta_chars")
    expect(page).not.toContain("parseFloat")
    expect(page).not.toContain("CatalogCreateForm")
    expect(page).not.toContain("acceptExtraction")
  })
})
