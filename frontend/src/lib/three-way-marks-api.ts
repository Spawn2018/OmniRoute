import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ThreeWayMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  way_kind: string
  source_ref: string
}

export type ThreeWayMarkPayload = {
  mark_code: string
  way_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/three-way-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeThreeWayMarkPayload(
  markCode: string,
  wayKind: string,
  sourceRef: string,
): ThreeWayMarkPayload {
  return {
    mark_code: markCode.trim(),
    way_kind: wayKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadThreeWayMarks(): Promise<ThreeWayMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog 3-way niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ThreeWayMarkRow[]
}

export async function createThreeWayMark(
  payload: ThreeWayMarkPayload,
): Promise<ThreeWayMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "three-way-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika 3-way odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ThreeWayMarkRow
}
