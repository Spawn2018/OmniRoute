import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SuggestionLedgerRow = {
  id: string
  organization_id: string
  target_bc: string
  entity_id: string
  suggestion_kind: string
  interval_low: string
  interval_high: string
  model_version: string
  prompt_version: string
  reaction: string
  changed_to: string
  source_ref: string
}

export type SuggestionLedgerPayload = {
  target_bc: string
  entity_id: string
  suggestion_kind: string
  interval_low: string
  interval_high: string
  model_version: string
  prompt_version: string
  reaction: string
  changed_to: string
  source_ref: string
}

const ENDPOINT = "/api/v1/suggestion-ledgers" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeSuggestionLedgerPayload(draft: {
  targetBc: string
  entityId: string
  kind: string
  intervalLow: string
  intervalHigh: string
  modelVersion: string
  promptVersion: string
  reaction: string
  changedTo: string
  sourceRef: string
}): SuggestionLedgerPayload {
  return {
    target_bc: draft.targetBc.trim(),
    entity_id: draft.entityId.trim(),
    suggestion_kind: draft.kind.trim().toLowerCase(),
    interval_low: draft.intervalLow.trim(),
    interval_high: draft.intervalHigh.trim(),
    model_version: draft.modelVersion.trim(),
    prompt_version: draft.promptVersion.trim(),
    reaction: draft.reaction.trim().toLowerCase(),
    changed_to: draft.changedTo.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadSuggestionLedgers(): Promise<SuggestionLedgerRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog ledgeru podpowiedzi niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SuggestionLedgerRow[]
}

export async function createSuggestionLedger(
  payload: SuggestionLedgerPayload,
): Promise<SuggestionLedgerRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "suggestion-ledger-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis ledgeru podpowiedzi odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SuggestionLedgerRow
}
