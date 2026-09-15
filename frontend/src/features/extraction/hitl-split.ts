import type { ExtractionCandidate, ExtractionDraft } from "@/lib/extractions-api"

const CANDIDATE_PATCH_KINDS = new Set(["rate_line", "carrier_quote", "tender_rfp"])
const BULK_OK_BANDS = new Set(["green", "yellow", "high"])
const BULK_BAD_BANDS = new Set(["orange", "hold", "low", "poor"])
const BULK_MIN = 0.7

export function draftAllowsCandidatePatch(draftKind: string): boolean {
  return CANDIDATE_PATCH_KINDS.has(draftKind)
}

export function bulkAcceptConfidenceOk(raw: string | undefined): boolean {
  const token = (raw ?? "").trim().toLowerCase().replace(",", ".")
  if (token === "") {
    return false
  }
  if (BULK_OK_BANDS.has(token)) {
    return true
  }
  if (BULK_BAD_BANDS.has(token)) {
    return false
  }
  if (token.endsWith("%")) {
    const pct = Number(token.slice(0, -1).trim())
    return Number.isFinite(pct) && pct / 100 >= BULK_MIN
  }
  const value = Number(token)
  if (!Number.isFinite(value)) {
    return false
  }
  const ratio = value > 1 ? value / 100 : value
  return ratio >= BULK_MIN && ratio <= 1
}

export function bulkAcceptBlocked(candidates: ExtractionCandidate[]): boolean {
  return candidates.length >= 2 && candidates.some((row) => !bulkAcceptConfidenceOk(row.confidence_text))
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
  history: { revision: number; candidateCount: number }[]
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
    history: (draft.payload.history ?? []).map((entry) => ({
      revision: entry.revision,
      candidateCount: entry.candidates.length,
    })),
  }
}
