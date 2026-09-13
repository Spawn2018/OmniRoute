import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("silk_corridor_mark catalog", () => {
  it("maps plaster 470.0 to /silk-corridor-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["470.0"]).toBe("/silk-corridor-marks")
  })
})
