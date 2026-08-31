import {
  acceptExtractionDraftApiV1ExtractionsDraftIdAcceptPost,
  createExtractionDraftApiV1ExtractionsPost,
  listExtractionDraftsApiV1ExtractionsGet,
  rejectExtractionDraftApiV1ExtractionsDraftIdRejectPost,
} from "@/api/sdk.gen"
import type { ExtractRequest, ExtractionDraftResponse } from "@/api/types.gen"
import { ApiError } from "@/lib/api"
import { requireTenantHeaders } from "@/lib/tenant"

export type ExtractionCandidate = {
  code: string
  amount_text: string
  currency: string
  note?: string
}

export type ExtractionPayload = {
  source_ref: string
  unparsed_regions: string[]
  candidates: ExtractionCandidate[]
  parser_name?: string
  parser_challenger?: string | null
  ab_delta_chars?: number | null
}

export type ExtractionDraft = {
  id: string
  organization_id: string
  status: string
  source_ref: string
  input_text: string
  payload: ExtractionPayload
  reviewed_by: string | null
  reviewed_at: string | null
}

function statusOf(response: Response | undefined): number {
  return response?.status ?? 500
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
    })
  }
  const regionsRaw = Array.isArray(raw.unparsed_regions) ? raw.unparsed_regions : []
  return {
    source_ref: typeof raw.source_ref === "string" ? raw.source_ref : "",
    unparsed_regions: regionsRaw.filter((r): r is string => typeof r === "string"),
    candidates,
    parser_name: typeof raw.parser_name === "string" ? raw.parser_name : undefined,
    parser_challenger: typeof raw.parser_challenger === "string" ? raw.parser_challenger : null,
    ab_delta_chars: typeof raw.ab_delta_chars === "number" ? raw.ab_delta_chars : null,
  }
}

function toDraft(row: ExtractionDraftResponse): ExtractionDraft {
  return {
    id: row.id,
    organization_id: row.organization_id,
    status: row.status,
    source_ref: row.source_ref,
    input_text: row.input_text,
    payload: asPayload(row.payload),
    reviewed_by: row.reviewed_by,
    reviewed_at: row.reviewed_at,
  }
}

export async function fetchExtractionDrafts(status = "pending"): Promise<ExtractionDraft[]> {
  const { data, error, response } = await listExtractionDraftsApiV1ExtractionsGet({
    headers: requireTenantHeaders(),
    query: { status },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd listy ekstrakcji", statusOf(response))
  }
  return data.map(toDraft)
}

export async function createExtractionDraft(body: {
  source_ref: string
  input_text?: string
  document_base64?: string
}): Promise<ExtractionDraft> {
  const { data, error, response } = await createExtractionDraftApiV1ExtractionsPost({
    headers: requireTenantHeaders(),
    // openapi-ts spłaszcza anyOf|null — payload XOR idzie w JSON
    body: body as ExtractRequest,
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd ekstrakcji", statusOf(response))
  }
  return toDraft(data)
}

export async function acceptExtractionDraft(draftId: string): Promise<ExtractionDraft> {
  const { data, error, response } = await acceptExtractionDraftApiV1ExtractionsDraftIdAcceptPost({
    headers: requireTenantHeaders(),
    path: { draft_id: draftId },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd akceptacji", statusOf(response))
  }
  return toDraft(data)
}

export async function rejectExtractionDraft(draftId: string): Promise<ExtractionDraft> {
  const { data, error, response } = await rejectExtractionDraftApiV1ExtractionsDraftIdRejectPost({
    headers: requireTenantHeaders(),
    path: { draft_id: draftId },
  })
  if (error || !data) {
    throw new ApiError(JSON.stringify(error) || "Błąd odrzucenia", statusOf(response))
  }
  return toDraft(data)
}
