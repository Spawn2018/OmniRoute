import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AllocationKeyRow = {
  id: string
  organization_id: string
  key_code: string
  source_ref: string
}

export type AllocationKeyPayload = {
  key_code: string
  source_ref: string
}

const ENDPOINT = "/api/v1/allocation-keys" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeAllocationKeyPayload(draft: {
  keyCode: string
  sourceRef: string
}): AllocationKeyPayload {
  return {
    key_code: draft.keyCode.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadAllocationKeys(): Promise<AllocationKeyRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog klucza alokacji niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as AllocationKeyRow[]
}

export async function createAllocationKey(
  payload: AllocationKeyPayload,
): Promise<AllocationKeyRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "allocation-key-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis klucza alokacji odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as AllocationKeyRow
}
