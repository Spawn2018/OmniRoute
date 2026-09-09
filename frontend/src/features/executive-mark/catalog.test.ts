import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { briefWrite } from "@/lib/executive-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("briefWrite", () => {
  it("trims question without money math or summing", () => {
    expect(briefWrite({ askKind: " lane ", originRef: "tenant:manual" })).toEqual({
      question_kind: "lane",
      source_ref: "tenant:manual",
    })
  })
})

describe("executive_mark surface for 202.0", () => {
  it("records a HITL question on /executive-marks without Money or summing", () => {
    const page = src("features/executive-mark/catalog-page.tsx")
    const stage = src("features/executive-mark/brief-stage.tsx")
    expect(src("routes/executive-marks.tsx")).toContain("/executive-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/executive-marks"')
    expect(src("lib/business-lists.ts")).toContain("executiveMark")
    expect(page).toContain('data-executive-mark="desk"')
    expect(page).toContain("BriefStage")
    expect(stage).toContain("persistBriefMark")
    expect(stage).not.toContain("<Money")
    expect(stage).toContain("Zapisz pytanie zarządu")
    expect(stage).not.toContain("parseFloat")
    expect(stage).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"202.0": "/executive-marks"')
  })
})
