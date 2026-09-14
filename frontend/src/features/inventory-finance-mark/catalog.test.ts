import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildInventoryFinanceMarkWrite } from "@/lib/inventory-finance-marks-api"

describe("inventory_finance_mark catalog", () => {
  it("maps plaster 476.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["476.0"]).toBe("/inventory-finance-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildInventoryFinanceMarkWrite({
        code: " inv_release_01 ",
        kind: " Release ",
        origin: " fixture://inventory-finance/1 ",
      }),
    ).toEqual({
      mark_code: "inv_release_01",
      finance_kind: "release",
      source_ref: "fixture://inventory-finance/1",
    })
  })
})
