import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildLineImpactLayerMarkWrite } from "@/lib/line-impact-layer-marks-api"

describe("line_impact_layer_mark catalog", () => {
  it("maps plaster 479.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["479.0"]).toBe("/line-impact-layer-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildLineImpactLayerMarkWrite({
        code: " lil_scored_01 ",
        kind: " Scored ",
        origin: " fixture://line-impact-layer/1 ",
      }),
    ).toEqual({
      mark_code: "lil_scored_01",
      layer_kind: "scored",
      source_ref: "fixture://line-impact-layer/1",
    })
  })
})
