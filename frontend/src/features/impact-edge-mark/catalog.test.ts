import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("impact-edge-mark shipped route", () => {
  it("maps 520.0 to impact-edge-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["520.0"]).toBe("/impact-edge-marks")
  })
})
