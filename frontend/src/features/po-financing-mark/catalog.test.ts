import { describe, expect, it } from "vitest"
import { buildPoFinancingMarkWrite } from "@/lib/po-financing-marks-api"

describe("buildPoFinancingMarkWrite", () => {
  it("trims mark fields", () => {
    expect(
      buildPoFinancingMarkWrite({
        code: " po_trade_01 ",
        kind: " Release ",
        origin: " fixture://po-financing/1 ",
      }),
    ).toEqual({
      mark_code: "po_trade_01",
      financing_kind: "release",
      source_ref: "fixture://po-financing/1",
    })
  })
})
