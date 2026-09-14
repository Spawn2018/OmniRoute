import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildQualityDescentMarkWrite } from "@/lib/quality-descent-marks-api"

describe("quality_descent_mark catalog", () => {
  it("maps plaster 486.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["486.0"]).toBe("/quality-descent-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildQualityDescentMarkWrite({
        code: " qd_crps_01 ",
        kind: " Crps ",
        origin: " fixture://quality-descent/1 ",
      }),
    ).toEqual({
      mark_code: "qd_crps_01",
      descent_kind: "crps",
      source_ref: "fixture://quality-descent/1",
    })
  })
})
