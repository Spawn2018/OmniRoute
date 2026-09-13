import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { BUSINESS_LISTS } from "@/lib/business-lists"

describe("BR3.3 tacho constraint catalog", () => {
  it("binds plaster 465.0 to the plan-constraint desk", () => {
    expect(SHIPPED_CHARGE_ROUTES["465.0"]).toBe("/tacho-plan-marks")
    expect(BUSINESS_LISTS.tachoPlanMark.route).toBe("/tacho-plan-marks")
    expect(BUSINESS_LISTS.tachoPlanMark.tableKey).toBe("tacho_plan_mark")
  })
})
