import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildShipmentCloneMarkWrite } from "@/lib/shipment-clone-marks-api"

describe("shipment_clone_mark catalog", () => {
  it("maps plaster 528.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["528.0"]).toBe("/shipment-clone-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildShipmentCloneMarkWrite({
        code: " clone_last_01 ",
        kind: " Last_Similar ",
        origin: " fixture://shipment-clone-mark/1 ",
      }),
    ).toEqual({
      mark_code: "clone_last_01",
      clone_kind: "last_similar",
      source_ref: "fixture://shipment-clone-mark/1",
    })
  })
})
