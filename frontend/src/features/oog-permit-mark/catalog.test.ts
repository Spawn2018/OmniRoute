import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("BR4.1 OOG permit catalog", () => {
  it("ships plaster 467.0 to the permit desk", () => {
    expect(SHIPPED_CHARGE_ROUTES["467.0"]).toBe("/oog-permit-marks")
    expect(SHIPPED_CHARGE_ROUTES["326.0"]).toBe("/oog-marks")
  })
})
