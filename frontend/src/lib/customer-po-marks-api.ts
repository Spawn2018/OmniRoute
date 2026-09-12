import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CustomerPoMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  ref_kind: string
  source_ref: string
}

export type CustomerPoMarkPayload = {
  mark_code: string
  ref_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/customer-po-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeCustomerPoMarkPayload(
  markCode: string,
  refKind: string,
  sourceRef: string,
): CustomerPoMarkPayload {
  return {
    mark_code: markCode.trim(),
    ref_kind: refKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadCustomerPoMarks(): Promise<CustomerPoMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog referencji PO klienta niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CustomerPoMarkRow[]
}

export async function createCustomerPoMark(
  payload: CustomerPoMarkPayload,
): Promise<CustomerPoMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "customer-po-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika referencji PO klienta odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CustomerPoMarkRow
}
