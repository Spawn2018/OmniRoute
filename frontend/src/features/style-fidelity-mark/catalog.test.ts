import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildStyleFidelityMarkWrite } from "@/lib/style-fidelity-marks-api"

describe("style_fidelity_mark catalog", () => {
  it("maps plaster 485.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["485.0"]).toBe("/style-fidelity-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildStyleFidelityMarkWrite({
        code: " fid_hold_01 ",
        kind: " Hold ",
        origin: " fixture://style-fidelity/1 ",
      }),
    ).toEqual({
      mark_code: "fid_hold_01",
      fidelity_kind: "hold",
      source_ref: "fixture://style-fidelity/1",
    })
  })
})
