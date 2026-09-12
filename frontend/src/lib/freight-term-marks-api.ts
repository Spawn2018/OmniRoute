import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FreightTermMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  term_kind: string
  source_ref: string
}

export type FreightTermMarkPayload = {
  mark_code: string
  term_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/freight-term-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeFreightTermMarkPayload(
  markCode: string,
  termKind: string,
  sourceRef: string,
): FreightTermMarkPayload {
  return {
    mark_code: markCode.trim(),
    term_kind: termKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadFreightTermMarks(): Promise<FreightTermMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog warunku frachtu niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FreightTermMarkRow[]
}

export async function createFreightTermMark(
  payload: FreightTermMarkPayload,
): Promise<FreightTermMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "freight-term-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika warunku frachtu odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FreightTermMarkRow
}
