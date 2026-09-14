import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildInventoryCollateralMarkWrite } from "@/lib/inventory-collateral-marks-api"

describe("inventory_collateral_mark catalog", () => {
  it("maps plaster 477.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["477.0"]).toBe("/inventory-collateral-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildInventoryCollateralMarkWrite({
        code: " col_pledge_01 ",
        kind: " Pledge ",
        origin: " fixture://inventory-collateral/1 ",
      }),
    ).toEqual({
      mark_code: "col_pledge_01",
      collateral_kind: "pledge",
      source_ref: "fixture://inventory-collateral/1",
    })
  })
})
