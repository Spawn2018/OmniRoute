import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { describe, expect, it } from "vitest"

describe("580.0 container unload date", () => {
  it("locks SHIPPED to shipments", () => {
    expect(SHIPPED_CHARGE_ROUTES["580.0"]).toBe("/shipments")
  })
})
