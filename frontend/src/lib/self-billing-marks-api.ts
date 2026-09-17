import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/self-billing-marks"

export type SelfBillingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  billing_kind: string
  source_ref: string
}

export type SelfBillingMarkWrite = {
  mark_code: string
  billing_kind: string
  source_ref: string
}

export function buildSelfBillingMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): SelfBillingMarkWrite {
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

export async function fetchSelfBillingMarks(): Promise<SelfBillingMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników self-billing", 200)
}

export async function saveSelfBillingMark(
  body: SelfBillingMarkWrite,
): Promise<SelfBillingMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika self-billing", 201)
}
