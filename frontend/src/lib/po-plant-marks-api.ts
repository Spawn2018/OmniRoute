import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PoPlantMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  plant_kind: string
  source_ref: string
}

export type PoPlantMarkPayload = {
  mark_code: string
  plant_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/po-plant-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makePoPlantMarkPayload(
  markCode: string,
  plantKind: string,
  sourceRef: string,
): PoPlantMarkPayload {
  return {
    mark_code: markCode.trim(),
    plant_kind: plantKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadPoPlantMarks(): Promise<PoPlantMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog po plant niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PoPlantMarkRow[]
}

export async function createPoPlantMark(
  payload: PoPlantMarkPayload,
): Promise<PoPlantMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "po-plant-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika po plant odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PoPlantMarkRow
}
