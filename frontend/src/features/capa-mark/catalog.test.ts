import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { buildCapaWrite } from "@/lib/capa-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("buildCapaWrite", () => {
  it("trims HITL fields and lowercases kind", () => {
    expect(
      buildCapaWrite({
        code: " capa_pl_01 ",
        kind: " Eight_D ",
        origin: "tenant:manual",
      }),
    ).toEqual({
      mark_code: "capa_pl_01",
      mark_kind: "eight_d",
      source_ref: "tenant:manual",
    })
  })
})

describe("capa_mark surface for 282.0", () => {
  it("records HITL mark on /capa-marks without money fields", () => {
    const page = src("features/capa-mark/catalog-page.tsx")
    const panel = src("features/capa-mark/capa-mark-form.tsx")
    const client = src("lib/capa-marks-api.ts")
    expect(src("routes/capa-marks.tsx")).toContain("/capa-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/capa-marks"')
    expect(src("lib/business-lists.ts")).toContain("capaMark")
    expect(page).toContain('data-capa-mark="board"')
    expect(page).toContain("CapaMarkDesk")
    expect(panel).toContain("saveCapaMark")
    expect(panel).toContain("Zapisz znacznik CAPA")
    expect(panel).not.toContain("<Money")
    expect(client).not.toContain("shipment_id")
    expect(client).not.toContain("workflow_id")
    expect(src("features/ops/ops-index.ts")).toContain('"282.0": "/capa-marks"')
  })
})
