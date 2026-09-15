import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildKpiDefinitionMarkWrite } from "@/lib/kpi-definition-marks-api"

describe("kpi_definition_mark catalog", () => {
  it("maps plaster 526.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["526.0"]).toBe("/kpi-definition-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildKpiDefinitionMarkWrite({
        code: " kpi_otd_01 ",
        kind: " Otd ",
        origin: " fixture://kpi-definition-mark/1 ",
      }),
    ).toEqual({
      mark_code: "kpi_otd_01",
      kpi_kind: "otd",
      source_ref: "fixture://kpi-definition-mark/1",
    })
  })
})
