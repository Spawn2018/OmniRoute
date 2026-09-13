import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OutcomeKindRow = {
  id: string
  organization_id: string
  kind_code: string
  source_ref: string
}

export type OutcomeKindPayload = {
  kind_code: string
  source_ref: string
}

const ENDPOINT = "/api/v1/outcome-kinds" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeOutcomeKindPayload(draft: {
  kindCode: string
  sourceRef: string
}): OutcomeKindPayload {
  return {
    kind_code: draft.kindCode.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadOutcomeKinds(): Promise<OutcomeKindRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog rodzaju wyniku niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OutcomeKindRow[]
}

export async function createOutcomeKind(
  payload: OutcomeKindPayload,
): Promise<OutcomeKindRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "outcome-kind-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis rodzaju wyniku odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OutcomeKindRow
}
