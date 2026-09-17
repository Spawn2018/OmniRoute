import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { describe, expect, it } from "vitest"

describe("purchase-invoice catalog", () => {
  it("ships 549.0 to purchase-invoices", () => {
    expect(SHIPPED_CHARGE_ROUTES["549.0"]).toBe("/purchase-invoices")
  })
})
