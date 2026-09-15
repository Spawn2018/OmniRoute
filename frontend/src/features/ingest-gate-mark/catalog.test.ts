import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildIngestGateMarkWrite } from "@/lib/ingest-gate-marks-api"

describe("ingest_gate_mark catalog", () => {
  it("maps plaster 523.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["523.0"]).toBe("/ingest-gate-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildIngestGateMarkWrite({
        code: " ig_truth_01 ",
        kind: " Truth ",
        origin: " fixture://ingest-gate-mark/1 ",
      }),
    ).toEqual({
      mark_code: "ig_truth_01",
      gate_kind: "truth",
      source_ref: "fixture://ingest-gate-mark/1",
    })
  })
})
