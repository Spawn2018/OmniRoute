import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OutcomeLedgerRow = {
  id: string
  organization_id: string
  target_bc: string
  entity_id: string
  suggestion_id: string
  outcome_kind: string
  actual_value: string
  source_ref: string
}

export type OutcomeLedgerPayload = {
  target_bc: string
  entity_id: string
  suggestion_id: string
  outcome_kind: string
  actual_value: string
  source_ref: string
}

const ENDPOINT = "/api/v1/outcome-ledgers" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeOutcomeLedgerPayload(draft: {
  targetBc: string
  entityId: string
  suggestionId: string
  kind: string
  actualValue: string
  sourceRef: string
}): OutcomeLedgerPayload {
  return {
    target_bc: draft.targetBc.trim(),
    entity_id: draft.entityId.trim(),
    suggestion_id: draft.suggestionId.trim(),
    outcome_kind: draft.kind.trim().toLowerCase(),
    actual_value: draft.actualValue.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadOutcomeLedgers(): Promise<OutcomeLedgerRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog ledgeru wyniku niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OutcomeLedgerRow[]
}

export async function createOutcomeLedger(
  payload: OutcomeLedgerPayload,
): Promise<OutcomeLedgerRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "outcome-ledger-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis ledgeru wyniku odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OutcomeLedgerRow
}
