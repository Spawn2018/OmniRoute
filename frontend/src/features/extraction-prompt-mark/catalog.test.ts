import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("extraction-prompt-mark catalog", () => {
  it("ships 502.0 under /extraction-prompt-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["502.0"]).toBe("/extraction-prompt-marks")
  })
})
