import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PaymentTermsMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  terms_kind: string
  source_ref: string
}

export type PaymentTermsMarkPayload = {
  mark_code: string
  terms_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/payment-terms-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makePaymentTermsMarkPayload(
  markCode: string,
  termsKind: string,
  sourceRef: string,
): PaymentTermsMarkPayload {
  return {
    mark_code: markCode.trim(),
    terms_kind: termsKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadPaymentTermsMarks(): Promise<PaymentTermsMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog warunkow platnosci niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PaymentTermsMarkRow[]
}

export async function createPaymentTermsMark(
  payload: PaymentTermsMarkPayload,
): Promise<PaymentTermsMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "payment-terms-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika warunkow platnosci odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PaymentTermsMarkRow
}
