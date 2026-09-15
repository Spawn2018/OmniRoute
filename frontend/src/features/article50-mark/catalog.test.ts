import { describe, expect, it } from "vitest"
import { SHIPPED_CHARGE_ROUTES } from "@/features/ops/ops-index"
import { buildArticle50MarkWrite } from "@/lib/article50-marks-api"

describe("article50_mark catalog", () => {
  it("maps plaster 521.0 to route", () => {
    expect(SHIPPED_CHARGE_ROUTES["521.0"]).toBe("/article50-marks")
  })

  it("trims mark fields", () => {
    expect(
      buildArticle50MarkWrite({
        code: " a50_generated_01 ",
        kind: " Generated ",
        origin: " fixture://article50-mark/1 ",
      }),
    ).toEqual({
      mark_code: "a50_generated_01",
      label_kind: "generated",
      source_ref: "fixture://article50-mark/1",
    })
  })
})
