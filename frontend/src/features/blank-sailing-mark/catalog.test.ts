import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { BUSINESS_LISTS } from "@/lib/business-lists"
import { describe, expect, it } from "vitest"

describe("blank-sailing-mark catalog", () => {
  it("ships 565.0 on blank-sailing-marks", () => {
    expect(SHIPPED_CHARGE_ROUTES["565.0"]).toBe("/blank-sailing-marks")
    expect(BUSINESS_LISTS.blankSailingMark.route).toBe("/blank-sailing-marks")
  })
})
