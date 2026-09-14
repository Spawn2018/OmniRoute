import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildAutomationBiasMarkWrite } from "@/lib/automation-bias-marks-api"

describe("automation_bias_mark catalog", () => {
  it("maps plaster 482.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["482.0"]).toBe("/automation-bias-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildAutomationBiasMarkWrite({
        code: " ab_confirm_01 ",
        kind: " Confirm ",
        origin: " fixture://automation-bias/1 ",
      }),
    ).toEqual({
      mark_code: "ab_confirm_01",
      bias_kind: "confirm",
      source_ref: "fixture://automation-bias/1",
    })
  })
})
