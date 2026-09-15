import { createElement } from "react"
import { renderToStaticMarkup } from "react-dom/server"
import { describe, expect, it } from "vitest"
import { HitlReviewSplit } from "@/features/extraction/hitl-review-split"
import {
  HITL_AI_LABEL,
  bulkAcceptBlocked,
  bulkAcceptConfidenceOk,
  hitlGeneratedContentLabel,
  hitlSplitView,
} from "@/features/extraction/hitl-split"
import type { ExtractionDraft } from "@/lib/extractions-api"

function sampleDraft(): ExtractionDraft {
  return {
    id: "11111111-1111-1111-1111-111111111111",
    organization_id: "22222222-2222-2222-2222-222222222222",
    status: "pending",
    draft_kind: "rate_line",
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

  it("gates bulk accept below 0.70 confidence", () => {
    expect(bulkAcceptConfidenceOk("0.70")).toBe(true)
    expect(bulkAcceptConfidenceOk("0.69")).toBe(false)
    expect(bulkAcceptConfidenceOk("hold")).toBe(false)
    expect(
      bulkAcceptBlocked([
        { code: "THC", amount_text: "10", currency: "EUR", confidence_text: "0.90" },
        { code: "BAF", amount_text: "5", currency: "EUR", confidence_text: "0.40" },
      ]),
    ).toBe(true)
    expect(
      bulkAcceptBlocked([
        { code: "THC", amount_text: "10", currency: "EUR", confidence_text: "0.40" },
      ]),
    ).toBe(false)
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
    expect(view.revision).toBe(0)
    expect(view.extractPath).toBe("text")
    expect(hitlGeneratedContentLabel(view)).toBe(HITL_AI_LABEL)
  })

  it("does not mark empty HITL as generated content", () => {
    expect(hitlGeneratedContentLabel(hitlSplitView(null))).toBeNull()
  })

  it("fails if the draft review UI has no AI label", () => {
    const html = renderToStaticMarkup(
      createElement(HitlReviewSplit, {
        draft: sampleDraft(),
        pdfBase64: null,
        busy: false,
        onAccept: () => undefined,
        onReject: () => undefined,
      }),
    )
    expect(html).toContain(HITL_AI_LABEL)
    expect(html).toContain('data-generated-content="ai"')
    expect(html).toContain('role="status"')
    expect(html).toContain("data-hitl-span")
  })

  it("shows candidate edit fields when a save handler is provided", () => {
    const html = renderToStaticMarkup(
      createElement(HitlReviewSplit, {
        draft: sampleDraft(),
        pdfBase64: null,
        busy: false,
        onAccept: () => undefined,
        onReject: () => undefined,
        onPatchCandidates: () => undefined,
      }),
    )
    expect(html).toContain("Zapisz poprawkę")
    expect(html).toContain("Kod kandydata 1")
    expect(html).toContain("Kwota kandydata 1")
    expect(html).toContain("Ramka kandydata 1")
    expect(html).toContain("wersja 0")
    expect(html).toContain("text")
  })

  it("does not show the AI label when no draft is selected", () => {
    const html = renderToStaticMarkup(
      createElement(HitlReviewSplit, {
        draft: null,
        pdfBase64: null,
        busy: false,
        onAccept: () => undefined,
        onReject: () => undefined,
      }),
    )
    expect(html).not.toContain(HITL_AI_LABEL)
    expect(html).not.toContain("data-generated-content")
  })
})
