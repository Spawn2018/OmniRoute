import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/billing-marks"

export type BillingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  billing_kind: string
  source_ref: string
}

export type BillingMarkWrite = {
  mark_code: string
  billing_kind: string
  source_ref: string
}

export function buildBillingMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): BillingMarkWrite {
  return {
    mark_code: fields.code.trim(),
    billing_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchBillingMarks(): Promise<BillingMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników yard", 200)
}

export async function saveBillingMark(body: BillingMarkWrite): Promise<BillingMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika billingu", 201)
}
