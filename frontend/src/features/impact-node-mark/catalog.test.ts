import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("impact-node-mark shipped route", () => {
  it("maps 519.0 to impact-node-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["519.0"]).toBe("/impact-node-marks")
  })
})
