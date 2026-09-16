import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildHandoverSbarMarkWrite } from "@/lib/handover-sbar-marks-api"

describe("handover_sbar_mark catalog", () => {
  it("maps plaster 529.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["529.0"]).toBe("/handover-sbar-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildHandoverSbarMarkWrite({
        code: " sbar_sit_01 ",
        kind: " Situation ",
        origin: " fixture://handover-sbar-mark/1 ",
      }),
    ).toEqual({
      mark_code: "sbar_sit_01",
      sbar_kind: "situation",
      source_ref: "fixture://handover-sbar-mark/1",
    })
  })
})
