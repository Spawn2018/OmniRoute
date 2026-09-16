import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildTripBillMarkWrite } from "@/lib/trip-bill-marks-api"

describe("trip_bill_mark catalog", () => {
  it("maps plaster 530.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["530.0"]).toBe("/trip-bill-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildTripBillMarkWrite({
        code: " bill_ready_01 ",
        kind: " Ready ",
        origin: " fixture://trip-bill-mark/1 ",
      }),
    ).toEqual({
      mark_code: "bill_ready_01",
      bill_kind: "ready",
      source_ref: "fixture://trip-bill-mark/1",
    })
  })
})
