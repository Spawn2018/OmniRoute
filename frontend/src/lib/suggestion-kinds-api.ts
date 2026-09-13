import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SuggestionKindRow = {
  id: string
  organization_id: string
  kind_code: string
  source_ref: string
}

export type SuggestionKindPayload = {
  kind_code: string
  source_ref: string
}

const ENDPOINT = "/api/v1/suggestion-kinds" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeSuggestionKindPayload(draft: {
  kindCode: string
  sourceRef: string
}): SuggestionKindPayload {
  return {
    kind_code: draft.kindCode.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadSuggestionKinds(): Promise<SuggestionKindRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog rodzaju podpowiedzi niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SuggestionKindRow[]
}

export async function createSuggestionKind(
  payload: SuggestionKindPayload,
): Promise<SuggestionKindRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "suggestion-kind-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis rodzaju podpowiedzi odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SuggestionKindRow
}
