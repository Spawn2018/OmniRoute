import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"

describe("allocation-level shipped route", () => {
  it("maps 518.0 to allocation-levels", () => {
    expect(SHIPPED_CHARGE_ROUTES["518.0"]).toBe("/allocation-levels")
  })
})
