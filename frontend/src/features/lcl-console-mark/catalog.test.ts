import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("BR4.2 LCL console catalog", () => {
  it("ships plaster 468.0 to the console desk", () => {
    expect(SHIPPED_CHARGE_ROUTES["468.0"]).toBe("/lcl-console-marks")
  })
})
