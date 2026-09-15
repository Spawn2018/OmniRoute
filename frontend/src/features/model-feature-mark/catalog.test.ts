import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildModelFeatureMarkWrite } from "@/lib/model-feature-marks-api"

describe("model_feature_mark catalog", () => {
  it("maps plaster 524.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["524.0"]).toBe("/model-feature-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildModelFeatureMarkWrite({
        code: " mf_numeric_01 ",
        kind: " Numeric ",
        origin: " fixture://model-feature-mark/1 ",
      }),
    ).toEqual({
      mark_code: "mf_numeric_01",
      feature_kind: "numeric",
      source_ref: "fixture://model-feature-mark/1",
    })
  })
})
