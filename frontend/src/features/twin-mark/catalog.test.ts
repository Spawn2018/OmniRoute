import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { twinWrite } from "@/lib/twin-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("twinWrite", () => {
  it("trims kind without money math or physics", () => {
    expect(twinWrite({ kindStamp: " cargo ", originStamp: "tenant:manual" })).toEqual({
      twin_kind: "cargo",
      source_ref: "tenant:manual",
    })
  })
})

describe("twin_mark surface for 199.0", () => {
  it("records a HITL twin on /twin-marks without Money or physics", () => {
    const page = src("features/twin-mark/catalog-page.tsx")
    const panel = src("features/twin-mark/twin-form.tsx")
    expect(src("routes/twin-marks.tsx")).toContain("/twin-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/twin-marks"')
    expect(src("lib/business-lists.ts")).toContain("twinMark")
    expect(page).toContain('data-twin-mark="desk"')
    expect(page).toContain("TwinPanel")
    expect(panel).toContain("persistTwinMark")
    expect(panel).not.toContain("<Money")
    expect(panel).toContain("Zapisz bliźniaka")
    expect(panel).not.toContain("parseFloat")
    expect(panel).not.toContain("CatalogCreateForm")
    expect(src("features/ops/ops-index.ts")).toContain('"199.0": "/twin-marks"')
  })
})
