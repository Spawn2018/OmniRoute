import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildHandoverNoteWrite } from "@/lib/handover-notes-api"

describe("handover_note catalog", () => {
  it("maps plaster 543.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["543.0"]).toBe("/handover-notes")
  })

  it("trims note fields", () => {
    expect(
      buildHandoverNoteWrite({
        code: " shift_a_01 ",
        situation: " sit ",
        background: " back ",
        assessment: " assess ",
        recommendation: " rec ",
        origin: " fixture://handover-note/1 ",
      }),
    ).toEqual({
      note_code: "shift_a_01",
      situation: "sit",
      background: "back",
      assessment: "assess",
      recommendation: "rec",
      source_ref: "fixture://handover-note/1",
    })
  })
})
