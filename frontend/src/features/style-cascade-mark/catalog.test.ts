import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildStyleCascadeMarkWrite } from "@/lib/style-cascade-marks-api"

describe("style_cascade_mark catalog", () => {
  it("maps plaster 484.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["484.0"]).toBe("/style-cascade-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildStyleCascadeMarkWrite({
        code: " style_user_01 ",
        kind: " Person ",
        origin: " fixture://style-cascade/1 ",
      }),
    ).toEqual({
      mark_code: "style_user_01",
      cascade_kind: "person",
      source_ref: "fixture://style-cascade/1",
    })
  })
})
