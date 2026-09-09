import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { carbonWrite } from "@/lib/tender-carbon-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("carbonWrite", () => {
  it("trims carbon-mark fields without money or kg math", () => {
    expect(
      carbonWrite({
        boardStamp: " 11111111-1111-1111-1111-111111111111 ",
        markStamp: " exempt ",
        originStamp: "tenant:manual",
      }),
    ).toEqual({
      tender_id: "11111111-1111-1111-1111-111111111111",
      mark_code: "exempt",
      source_ref: "tenant:manual",
    })
  })
})

describe("tender_carbon_mark surface for 184.0", () => {
  it("records a carbon mark on /tender-carbon-marks without kg or amount", () => {
    const page = src("features/tender-carbon-mark/catalog-page.tsx")
    const panel = src("features/tender-carbon-mark/mark-form.tsx")
    expect(src("routes/tender-carbon-marks.tsx")).toContain("/tender-carbon-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/tender-carbon-marks"')
    expect(src("lib/business-lists.ts")).toContain("tenderCarbonMark")
    expect(page).toContain('data-tender-carbon-mark="desk"')
    expect(page).toContain("CarbonPanel")
    expect(panel).toContain("persistCarbonMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz znacznik śladu")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("leaflet")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"184.0": "/tender-carbon-marks"')
  })
})
