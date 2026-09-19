import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { describe, expect, it } from "vitest"

describe("583.0 container needs external power", () => {
  it("locks SHIPPED to shipments", () => {
    expect(SHIPPED_CHARGE_ROUTES["583.0"]).toBe("/shipments")
  })
})
