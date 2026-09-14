import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildL3GateMarkWrite } from "@/lib/l3-gate-marks-api"

describe("l3_gate_mark catalog", () => {
  it("maps plaster 483.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["483.0"]).toBe("/l3-gate-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildL3GateMarkWrite({
        code: " l3_sot_01 ",
        kind: " Owner ",
        origin: " fixture://l3-gate/1 ",
      }),
    ).toEqual({
      mark_code: "l3_sot_01",
      gate_kind: "owner",
      source_ref: "fixture://l3-gate/1",
    })
  })
})
