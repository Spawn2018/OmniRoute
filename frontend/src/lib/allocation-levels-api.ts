import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AllocationLevelRow = {
  id: string
  organization_id: string
  level_code: string
  source_ref: string
}

export type AllocationLevelPayload = {
  level_code: string
  source_ref: string
}

const ENDPOINT = "/api/v1/allocation-levels" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeAllocationLevelPayload(draft: {
  levelCode: string
  sourceRef: string
}): AllocationLevelPayload {
  return {
    level_code: draft.levelCode.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadAllocationLevels(): Promise<AllocationLevelRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog poziomu alokacji niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as AllocationLevelRow[]
}

export async function createAllocationLevel(
  payload: AllocationLevelPayload,
): Promise<AllocationLevelRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "allocation-level-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis poziomu alokacji odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as AllocationLevelRow
}
