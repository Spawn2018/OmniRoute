import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AutonomyLevelRow = {
  id: string
  organization_id: string
  level_code: string
  source_ref: string
}

export type AutonomyLevelPayload = {
  level_code: string
  source_ref: string
}

const ENDPOINT = "/api/v1/autonomy-levels" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeAutonomyLevelPayload(draft: {
  levelCode: string
  sourceRef: string
}): AutonomyLevelPayload {
  return {
    level_code: draft.levelCode.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadAutonomyLevels(): Promise<AutonomyLevelRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog poziomu autonomii niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as AutonomyLevelRow[]
}

export async function createAutonomyLevel(
  payload: AutonomyLevelPayload,
): Promise<AutonomyLevelRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "autonomy-level-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis poziomu autonomii odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as AutonomyLevelRow
}
