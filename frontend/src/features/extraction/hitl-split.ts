import type { ExtractionCandidate, ExtractionDraft } from "@/lib/extractions-api"

const CANDIDATE_PATCH_KINDS = new Set(["rate_line", "carrier_quote", "tender_rfp"])

export function draftAllowsCandidatePatch(draftKind: string): boolean {
  return CANDIDATE_PATCH_KINDS.has(draftKind)
}

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
  revision: number
  extractPath: string
}

export type HitlSplitView = HitlSplitEmpty | HitlSplitReview

export const HITL_AI_LABEL = "propozycja AI"

export function hitlGeneratedContentLabel(view: HitlSplitView): string | null {
  return view.kind === "review" ? HITL_AI_LABEL : null
}

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
    revision: draft.payload.revision ?? 0,
    extractPath: draft.payload.extract_path ?? "text",
  }
}
