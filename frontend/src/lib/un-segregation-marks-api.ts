import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type UnSegregationMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  segregate_kind: string
  source_ref: string
}

export type UnSegregationMarkPayload = {
  mark_code: string
  segregate_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/un-segregation-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeUnSegregationMarkPayload(
  markCode: string,
  segregateKind: string,
  sourceRef: string,
): UnSegregationMarkPayload {
  return {
    mark_code: markCode.trim(),
    segregate_kind: segregateKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadUnSegregationMarks(): Promise<UnSegregationMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog segregacji UN niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as UnSegregationMarkRow[]
}

export async function createUnSegregationMark(
  payload: UnSegregationMarkPayload,
): Promise<UnSegregationMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "un-segregation-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika segregacji UN odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as UnSegregationMarkRow
}
