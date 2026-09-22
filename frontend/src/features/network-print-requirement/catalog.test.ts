import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("D9c network print requirement catalog", () => {
  it("ships plaster 626.0 to the print requirement desk", () => {
    expect(SHIPPED_CHARGE_ROUTES["626.0"]).toBe("/network-print-requirements")
  })
})
