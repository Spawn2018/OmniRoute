import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildRfidMarkWrite } from "@/lib/rfid-marks-api"

describe("rfid_mark catalog", () => {
  it("maps plaster 475.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["475.0"]).toBe("/rfid-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildRfidMarkWrite({
        code: " rfid_gate_01 ",
        kind: " Gate ",
        origin: " fixture://rfid/1 ",
      }),
    ).toEqual({
      mark_code: "rfid_gate_01",
      rfid_kind: "gate",
      source_ref: "fixture://rfid/1",
    })
  })
})
