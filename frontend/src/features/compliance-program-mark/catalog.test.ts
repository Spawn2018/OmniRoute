import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildComplianceProgramMarkWrite } from "@/lib/compliance-program-marks-api"

describe("compliance_program_mark catalog", () => {
  it("maps plaster 488.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["488.0"]).toBe("/compliance-program-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildComplianceProgramMarkWrite({
        code: " cp_review_01 ",
        kind: " Review ",
        origin: " fixture://compliance-program/1 ",
      }),
    ).toEqual({
      mark_code: "cp_review_01",
      program_kind: "review",
      source_ref: "fixture://compliance-program/1",
    })
  })
})
