import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildWmsFlowMarkWrite } from "@/lib/wms-flow-marks-api"

describe("wms_flow_mark catalog", () => {
  it("maps plaster 474.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["474.0"]).toBe("/wms-flow-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildWmsFlowMarkWrite({
        code: " wms_receipt_01 ",
        kind: " Receipt ",
        origin: " fixture://wms-flow/1 ",
      }),
    ).toEqual({
      mark_code: "wms_receipt_01",
      flow_kind: "receipt",
      source_ref: "fixture://wms-flow/1",
    })
  })
})
