import {
  acceptExtractionDraftApiV1ExtractionsDraftIdAcceptPost,
  createExtractionDraftApiV1ExtractionsPost,
  listExtractionDraftsApiV1ExtractionsGet,
  patchExtractionDraftApiV1ExtractionsDraftIdPatch,
  rejectExtractionDraftApiV1ExtractionsDraftIdRejectPost,
} from "@/api/sdk.gen"
import type { ExtractRequest, ExtractionDraftResponse } from "@/api/types.gen"
import { ApiError, httpErrorStatus } from "@/lib/api"

export type ExtractionCandidate = {
  code: string
  amount_text: string
  currency: string
  note?: string
  bbox_text?: string
  confidence_text?: string
}

export type ExtractionHistoryEntry = {
  revision: number
  candidates: ExtractionCandidate[]
}

export type ExtractionPayload = {
  source_ref: string
  unparsed_regions: string[]
  candidates: ExtractionCandidate[]
  parser_name?: string
  parser_challenger?: string | null
  ab_delta_chars?: number | null
  revision?: number
  extract_path?: string
  history?: ExtractionHistoryEntry[]
}

export type ExtractionDraft = {
  id: string
  organization_id: string
  status: string
  draft_kind: string
  source_ref: string
  input_text: string
  payload: ExtractionPayload
  reviewed_by: string | null
  reviewed_at: string | null
}

export function extractionCreateBody(args: {
  sourceRef: string
  inputText: string
  documentBase64: string | null
  draftKind?: string
  quote?: {
    party_id: string
    origin_port_id: string
    destination_port_id: string
    quote_date: string
    amount: string
    currency: string
    transit_days?: number
  }
  rfp?: {
    tender_id: string
    intake_code: string
  }
  extractPath?: string
}): {
  source_ref: string
  input_text?: string
  document_base64?: string
  draft_kind?: string
  extract_path?: string
  quote?: (typeof args)["quote"]
  rfp?: (typeof args)["rfp"]
} {
  const body: {
    source_ref: string
    input_text?: string
    document_base64?: string
    draft_kind?: string
    extract_path?: string
    quote?: (typeof args)["quote"]
    rfp?: (typeof args)["rfp"]
  } =
    args.documentBase64 !== null && args.documentBase64.length > 0
      ? { source_ref: args.sourceRef, document_base64: args.documentBase64 }
      : { source_ref: args.sourceRef, input_text: args.inputText }
  if (args.draftKind !== undefined && args.draftKind !== "") {
    body.draft_kind = args.draftKind
  }
  if (args.quote !== undefined) {
    body.quote = args.quote
  }
  if (args.rfp !== undefined) {
    body.rfp = args.rfp
  }
  if (args.extractPath !== undefined && args.extractPath !== "") {
    body.extract_path = args.extractPath
  }
  return body
}

function asPayload(raw: { [key: string]: unknown }): ExtractionPayload {
  const candidatesRaw = Array.isArray(raw.candidates) ? raw.candidates : []
  const candidates: ExtractionCandidate[] = []
  for (const entry of candidatesRaw) {
    if (typeof entry !== "object" || entry === null) {
      continue
    }
    const row = entry as Record<string, unknown>
    if (
      typeof row.code !== "string" ||
      typeof row.amount_text !== "string" ||
      typeof row.currency !== "string"
    ) {
      continue
    }
    candidates.push({
      code: row.code,
      amount_text: row.amount_text,
      currency: row.currency,
      note: typeof row.note === "string" ? row.note : undefined,
      bbox_text: typeof row.bbox_text === "string" ? row.bbox_text : undefined,
      confidence_text: typeof row.confidence_text === "string" ? row.confidence_text : undefined,
    })
  }
  const regionsRaw = Array.isArray(raw.unparsed_regions) ? raw.unparsed_regions : []
  const historyRaw = Array.isArray(raw.history) ? raw.history : []
  const history: ExtractionHistoryEntry[] = []
  for (const entry of historyRaw) {
    if (typeof entry !== "object" || entry === null) {
      continue
    }
    const row = entry as Record<string, unknown>
    if (typeof row.revision !== "number") {
      continue
    }
    const nested = asPayload({
      source_ref: "",
      unparsed_regions: [],
      candidates: Array.isArray(row.candidates) ? row.candidates : [],
    })
    history.push({ revision: row.revision, candidates: nested.candidates })
  }
  return {
    source_ref: typeof raw.source_ref === "string" ? raw.source_ref : "",
    unparsed_regions: regionsRaw.filter((r): r is string => typeof r === "string"),
    candidates,
    parser_name: typeof raw.parser_name === "string" ? raw.parser_name : undefined,
    parser_challenger: typeof raw.parser_challenger === "string" ? raw.parser_challenger : null,
    ab_delta_chars: typeof raw.ab_delta_chars === "number" ? raw.ab_delta_chars : null,
    revision: typeof raw.revision === "number" ? raw.revision : 0,
    extract_path: typeof raw.extract_path === "string" ? raw.extract_path : "text",
    history,
  }
}

function toDraft(row: ExtractionDraftResponse): ExtractionDraft {
  return {
    id: row.id,
    organization_id: row.organization_id,
    status: row.status,
    draft_kind: typeof row.draft_kind === "string" ? row.draft_kind : "rate_line",
    source_ref: row.source_ref,
    input_text: row.input_text,
    payload: asPayload(row.payload),
    reviewed_by: row.reviewed_by,
    reviewed_at: row.reviewed_at,
  }
}

export async function fetchExtractionDrafts(status = "pending"): Promise<ExtractionDraft[]> {
  const { data, error, response } = await listExtractionDraftsApiV1ExtractionsGet({
    query: { status },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd listy ekstrakcji", httpErrorStatus(response))
  }
  return data.map(toDraft)
}

export function aiProposals<Row extends { status: string }>(drafts: readonly Row[]): Row[] {
  return drafts.filter((row) => row.status === "pending")
}

export function qualityGaps<Row extends { payload: { unparsed_regions: readonly string[] } }>(
  drafts: readonly Row[],
): Row[] {
  return drafts.filter((row) => row.payload.unparsed_regions.length > 0)
}

export async function createExtractionDraft(body: {
  source_ref: string
  input_text?: string
  document_base64?: string
  extract_path?: string
  draft_kind?: string
}): Promise<ExtractionDraft> {
  const { data, error, response } = await createExtractionDraftApiV1ExtractionsPost({
    // openapi-ts spłaszcza anyOf|null — payload XOR idzie w JSON
    body: body as ExtractRequest,
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd ekstrakcji", httpErrorStatus(response))
  }
  return toDraft(data)
}

export async function patchExtractionCandidates(
  draftId: string,
  candidates: ExtractionCandidate[],
): Promise<ExtractionDraft> {
  const { data, error, response } = await patchExtractionDraftApiV1ExtractionsDraftIdPatch({
    path: { draft_id: draftId },
    body: { candidates },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd poprawki szkicu", httpErrorStatus(response))
  }
  return toDraft(data)
}

export async function acceptExtractionDraft(draftId: string): Promise<ExtractionDraft> {
  const { data, error, response } = await acceptExtractionDraftApiV1ExtractionsDraftIdAcceptPost({
    path: { draft_id: draftId },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd akceptacji", httpErrorStatus(response))
  }
  return toDraft(data)
}

export async function rejectExtractionDraft(draftId: string): Promise<ExtractionDraft> {
  const { data, error, response } = await rejectExtractionDraftApiV1ExtractionsDraftIdRejectPost({
    path: { draft_id: draftId },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd odrzucenia", httpErrorStatus(response))
  }
  return toDraft(data)
}
