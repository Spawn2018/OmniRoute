import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { describe, expect, it } from "vitest"

describe("610.0 container pol_unlocode", () => {
  it("locks SHIPPED to shipments", () => {
    expect(SHIPPED_CHARGE_ROUTES["610.0"]).toBe("/shipments")
  })
})
