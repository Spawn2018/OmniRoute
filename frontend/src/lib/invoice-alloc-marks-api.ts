import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/invoice-alloc-marks"

export type InvoiceAllocMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  alloc_kind: string
  source_ref: string
}

export type InvoiceAllocMarkWrite = {
  mark_code: string
  alloc_kind: string
  source_ref: string
}

export function buildInvoiceAllocMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): InvoiceAllocMarkWrite {
  return {
    mark_code: fields.code.trim(),
    alloc_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchInvoiceAllocMarks(): Promise<InvoiceAllocMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników alokacji FV", 200)
}

export async function saveInvoiceAllocMark(
  body: InvoiceAllocMarkWrite,
): Promise<InvoiceAllocMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika alokacji FV", 201)
}
