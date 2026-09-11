import { readFileSync } from "node:fs"
import { describe, expect, it } from "vitest"
import { buildFreightAuditWrite } from "@/lib/freight-audit-marks-api"

const src = (rel: string) => readFileSync(new URL(`../../${rel}`, import.meta.url), "utf8")

describe("buildFreightAuditWrite", () => {
  it("trims fields and lowercases kind", () => {
    expect(
      buildFreightAuditWrite({
        code: " audit_inv_01 ",
        kind: " Expected_Vs_Invoice ",
        origin: "tenant:manual",
      }),
    ).toEqual({
      mark_code: "audit_inv_01",
      audit_kind: "expected_vs_invoice",
      source_ref: "tenant:manual",
    })
  })
})

describe("freight_audit_mark surface for 283.0", () => {
  it("ships HITL catalog without money compare", () => {
    const page = src("features/freight-audit-mark/catalog-page.tsx")
    const panel = src("features/freight-audit-mark/freight-audit-mark-form.tsx")
    const client = src("lib/freight-audit-marks-api.ts")
    expect(src("routes/freight-audit-marks.tsx")).toContain("/freight-audit-marks")
    expect(src("components/layout/sidebar.tsx")).toContain('to: "/freight-audit-marks"')
    expect(src("lib/business-lists.ts")).toContain("freightAuditMark")
    expect(page).toContain("FreightAuditMarkDesk")
    expect(panel).toContain("saveFreightAuditMark")
    expect(panel).not.toContain("<Money")
    expect(client).not.toContain("margin")
    expect(src("features/ops/ops-index.ts")).toContain('"283.0": "/freight-audit-marks"')
  })
})
