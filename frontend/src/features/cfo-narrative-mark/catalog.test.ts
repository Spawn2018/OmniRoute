import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildCfoNarrativeMarkWrite } from "@/lib/cfo-narrative-marks-api"

describe("cfo_narrative_mark catalog", () => {
  it("maps plaster 525.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["525.0"]).toBe("/cfo-narrative-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildCfoNarrativeMarkWrite({
        code: " cfo_anomaly_01 ",
        kind: " Anomaly ",
        origin: " fixture://cfo-narrative-mark/1 ",
      }),
    ).toEqual({
      mark_code: "cfo_anomaly_01",
      narrative_kind: "anomaly",
      source_ref: "fixture://cfo-narrative-mark/1",
    })
  })
})
