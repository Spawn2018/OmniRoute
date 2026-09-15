import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildFieldConfidenceMarkWrite } from "@/lib/field-confidence-marks-api"

describe("field_confidence_mark catalog", () => {
  it("maps plaster 487.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["487.0"]).toBe("/field-confidence-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildFieldConfidenceMarkWrite({
        code: " fc_yellow_01 ",
        kind: " Yellow ",
        origin: " fixture://field-confidence/1 ",
      }),
    ).toEqual({
      mark_code: "fc_yellow_01",
      band_kind: "yellow",
      source_ref: "fixture://field-confidence/1",
    })
  })
})
