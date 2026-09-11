import { describe, expect, it } from "vitest"
import { readFileSync } from "node:fs"
import { otifMarkBody } from "@/lib/otif-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("otifMarkBody", () => {
  it("trims HITL fields and lowercases scope", () => {
    expect(
      otifMarkBody({
        markSlug: " otif_pickup_pl ",
        scopeKind: " Pickup ",
        originPointer: "tenant:manual",
      }),
    ).toEqual({
      mark_code: "otif_pickup_pl",
      scope_kind: "pickup",
      source_ref: "tenant:manual",
    })
  })
})

describe("otif_mark surface for 280.0", () => {
  it("records HITL mark on /otif-marks without OTIF% or money", () => {
    const page = src("features/otif-mark/catalog-page.tsx")
    const panel = src("features/otif-mark/otif-mark-form.tsx")
    const client = src("lib/otif-marks-api.ts")
    expect(src("routes/otif-marks.tsx")).toContain("/otif-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/otif-marks"')
    expect(src("lib/business-lists.ts")).toContain("otifMark")
    expect(page).toContain('data-otif-mark="board"')
    expect(page).toContain("OtifMarkDesk")
    expect(panel).toContain("persistOtifMark")
    expect(panel).toContain("Zapisz znacznik OTIF")
    expect(panel).not.toContain("<Money")
    expect(panel).not.toContain("OTIF%")
    expect(client).not.toContain("shipment_id")
    expect(client).not.toContain("otif_pct")
    expect(src("features/ops/ops-index.ts")).toContain('"280.0": "/otif-marks"')
  })
})
