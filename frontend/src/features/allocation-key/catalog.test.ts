import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("allocation-key shipped route", () => {
  it("maps 516.0 to allocation-keys", () => {
    expect(SHIPPED_CHARGE_ROUTES["516.0"]).toBe("/allocation-keys")
  })
})
