import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { describe, expect, it } from "vitest"

describe("582.0 container temp max", () => {
  it("locks SHIPPED to shipments", () => {
    expect(SHIPPED_CHARGE_ROUTES["582.0"]).toBe("/shipments")
  })
})
