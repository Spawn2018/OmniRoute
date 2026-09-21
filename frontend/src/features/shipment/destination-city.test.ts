import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("612.0 container destination_city", () => {
  it("locks shipped charge route to shipments", () => {
    expect(SHIPPED_CHARGE_ROUTES["612.0"]).toBe("/shipments")
  })
})
