import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { describe, expect, it } from "vitest"

describe("self-billing-mark catalog", () => {
  it("ships 548.0 to self-billing-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["548.0"]).toBe("/self-billing-marks")
  })
})
