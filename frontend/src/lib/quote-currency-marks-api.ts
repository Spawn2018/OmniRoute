import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type QuoteCurrencyMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  currency_kind: string
  source_ref: string
}

export type QuoteCurrencyMarkPayload = {
  mark_code: string
  currency_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/quote-currency-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeQuoteCurrencyMarkPayload(
  markCode: string,
  decisionKind: string,
  sourceRef: string,
): QuoteCurrencyMarkPayload {
  return {
    mark_code: markCode.trim(),
    currency_kind: decisionKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadQuoteCurrencyMarks(): Promise<QuoteCurrencyMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog quote currency niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as QuoteCurrencyMarkRow[]
}

export async function createQuoteCurrencyMark(
  payload: QuoteCurrencyMarkPayload,
): Promise<QuoteCurrencyMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "quote-currency-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika quote currency odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as QuoteCurrencyMarkRow
}
