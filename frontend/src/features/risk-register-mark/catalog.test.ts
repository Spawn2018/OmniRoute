import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildRiskRegisterMarkWrite } from "@/lib/risk-register-marks-api"

describe("risk_register_mark catalog", () => {
  it("maps plaster 481.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["481.0"]).toBe("/risk-register-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildRiskRegisterMarkWrite({
        code: " rr_open_01 ",
        kind: " Open ",
        origin: " fixture://risk-register/1 ",
      }),
    ).toEqual({
      mark_code: "rr_open_01",
      risk_kind: "open",
      source_ref: "fixture://risk-register/1",
    })
  })
})
