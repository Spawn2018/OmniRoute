import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { describe, expect, it } from "vitest"

describe("571.0 container payload_kg", () => {
  it("locks SHIPPED to shipments", () => {
    expect(SHIPPED_CHARGE_ROUTES["571.0"]).toBe("/shipments")
  })
})
