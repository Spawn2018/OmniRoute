import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/invoice-match-marks"

export type InvoiceMatchMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  match_kind: string
  source_ref: string
}

export type InvoiceMatchMarkWrite = {
  mark_code: string
  match_kind: string
  source_ref: string
}

export function buildInvoiceMatchMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): InvoiceMatchMarkWrite {
  return {
    mark_code: fields.code.trim(),
    match_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchInvoiceMatchMarks(): Promise<InvoiceMatchMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników match FV", 200)
}

export async function saveInvoiceMatchMark(
  body: InvoiceMatchMarkWrite,
): Promise<InvoiceMatchMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika match FV", 201)
}
