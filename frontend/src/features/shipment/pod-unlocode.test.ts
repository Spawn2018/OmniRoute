import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("611.0 container pod_unlocode", () => {
  it("locks shipped charge route to shipments", () => {
    expect(SHIPPED_CHARGE_ROUTES["611.0"]).toBe("/shipments")
  })
})
