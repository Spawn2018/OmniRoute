import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("nac_mark catalog", () => {
  it("maps plaster 469.0 to /nac-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["469.0"]).toBe("/nac-marks")
  })
})
