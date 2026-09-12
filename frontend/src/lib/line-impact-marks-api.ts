import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LineImpactMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  impact_kind: string
  source_ref: string
}

export type LineImpactMarkPayload = {
  mark_code: string
  impact_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/line-impact-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeLineImpactMarkPayload(
  markCode: string,
  impactKind: string,
  sourceRef: string,
): LineImpactMarkPayload {
  return {
    mark_code: markCode.trim(),
    impact_kind: impactKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadLineImpactMarks(): Promise<LineImpactMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog skutku linii niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as LineImpactMarkRow[]
}

export async function createLineImpactMark(
  payload: LineImpactMarkPayload,
): Promise<LineImpactMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "line-impact-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika skutku linii odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as LineImpactMarkRow
}
