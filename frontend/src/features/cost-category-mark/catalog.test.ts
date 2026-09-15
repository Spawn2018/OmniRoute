import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("cost-category-mark shipped route", () => {
  it("maps 517.0 to cost-category-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["517.0"]).toBe("/cost-category-marks")
  })
})
