import { describe, expect, it } from "vitest"
import { hitlSplitView } from "@/features/extraction/hitl-split"
import type { ExtractionDraft } from "@/lib/extractions-api"

function sampleDraft(): ExtractionDraft {
  return {
    id: "11111111-1111-1111-1111-111111111111",
    organization_id: "22222222-2222-2222-2222-222222222222",
    status: "pending",
    source_ref: "doc://tariff",
    input_text: "THC 100 EUR\nnote weekend",
    payload: {
      source_ref: "doc://tariff",
      unparsed_regions: ["note weekend"],
      candidates: [{ code: "THC", amount_text: "100", currency: "EUR" }],
    },
    reviewed_by: null,
    reviewed_at: null,
  }
}

describe("hitlSplitView", () => {
  it("returns empty when no draft is selected", () => {
    expect(hitlSplitView(null)).toEqual({ kind: "empty" })
  })

  it("puts source text in preview and candidates in the review pane", () => {
    const view = hitlSplitView(sampleDraft())
    expect(view.kind).toBe("review")
    if (view.kind !== "review") {
      return
    }
    expect(view.preview).toContain("THC 100 EUR")
    expect(view.candidates).toEqual([{ code: "THC", amount_text: "100", currency: "EUR" }])
    expect(view.unparsedRegions).toEqual(["note weekend"])
  })
})
