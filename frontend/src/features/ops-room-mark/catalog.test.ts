import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildOpsRoomMarkWrite } from "@/lib/ops-room-marks-api"

describe("ops_room_mark catalog", () => {
  it("maps plaster 478.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["478.0"]).toBe("/ops-room-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildOpsRoomMarkWrite({
        code: " ops_shift_01 ",
        kind: " Shift ",
        origin: " fixture://ops-room-mark/1 ",
      }),
    ).toEqual({
      mark_code: "ops_shift_01",
      layer_kind: "shift",
      source_ref: "fixture://ops-room-mark/1",
    })
  })
})
