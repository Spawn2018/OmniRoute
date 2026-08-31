import type { ExtractionCandidate, ExtractionDraft } from "@/lib/extractions-api"

export type HitlSplitEmpty = {
  kind: "empty"
}

export type HitlSplitReview = {
  kind: "review"
  draftId: string
  sourceRef: string
  preview: string
  candidates: ExtractionCandidate[]
  unparsedRegions: string[]
}

export type HitlSplitView = HitlSplitEmpty | HitlSplitReview

export function hitlSplitView(draft: ExtractionDraft | null): HitlSplitView {
  if (draft === null) {
    return { kind: "empty" }
  }
  return {
    kind: "review",
    draftId: draft.id,
    sourceRef: draft.source_ref,
    preview: draft.input_text,
    candidates: draft.payload.candidates,
    unparsedRegions: draft.payload.unparsed_regions,
  }
}
