import { describe, expect, it } from "vitest"
import { OPS_JOBS } from "@/features/ops/ops-index"
import { BUSINESS_LISTS } from "@/lib/business-lists"

describe("BR4.0 ferry reservation desk", () => {
  it("registers the booking catalog job on the ops board", () => {
    const job = OPS_JOBS.find((row) => row.route === "/ferry-booking-marks")
    expect(job?.label).toBe("Rezerwacja promu")
    expect(job?.job).toContain("ferry_booking_mark")
    expect(BUSINESS_LISTS.ferryBookingMark.tableKey).toBe("ferry_booking_mark")
  })
})
