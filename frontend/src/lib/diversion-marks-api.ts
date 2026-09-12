import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DiversionMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  stance_kind: string
  source_ref: string
}

export type DiversionMarkPayload = {
  mark_code: string
  stance_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/diversion-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeDiversionMarkPayload(
  markCode: string,
  stanceKind: string,
  sourceRef: string,
): DiversionMarkPayload {
  return {
    mark_code: markCode.trim(),
    stance_kind: stanceKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadDiversionMarks(): Promise<DiversionMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog diversion niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DiversionMarkRow[]
}

export async function createDiversionMark(
  payload: DiversionMarkPayload,
): Promise<DiversionMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "diversion-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika diversion odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DiversionMarkRow
}
