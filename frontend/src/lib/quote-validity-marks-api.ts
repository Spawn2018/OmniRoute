import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type QuoteValidityMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  validity_kind: string
  source_ref: string
}

export type QuoteValidityMarkPayload = {
  mark_code: string
  validity_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/quote-validity-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeQuoteValidityMarkPayload(
  markCode: string,
  validityKind: string,
  sourceRef: string,
): QuoteValidityMarkPayload {
  return {
    mark_code: markCode.trim(),
    validity_kind: validityKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadQuoteValidityMarks(): Promise<QuoteValidityMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog quote validity niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as QuoteValidityMarkRow[]
}

export async function createQuoteValidityMark(
  payload: QuoteValidityMarkPayload,
): Promise<QuoteValidityMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "quote-validity-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika quote validity odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as QuoteValidityMarkRow
}
