import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/company-marks"

export type CompanyMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  seat_kind: string
  source_ref: string
}

export type CompanyMarkWrite = {
  mark_code: string
  seat_kind: string
  source_ref: string
}

export function buildCompanyMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CompanyMarkWrite {
  return {
    mark_code: fields.code.trim(),
    seat_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCompanyMarks(): Promise<CompanyMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników spółki", 200)
}

export async function saveCompanyMark(body: CompanyMarkWrite): Promise<CompanyMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika spółki", 201)
}
