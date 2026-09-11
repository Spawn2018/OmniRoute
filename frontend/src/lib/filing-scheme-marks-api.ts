import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/filing-scheme-marks"

export type FilingSchemeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  scheme_kind: string
  source_ref: string
}

export type FilingSchemeMarkWrite = {
  mark_code: string
  scheme_kind: string
  source_ref: string
}

export function buildFilingSchemeMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): FilingSchemeMarkWrite {
  return {
    mark_code: fields.code.trim(),
    scheme_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchFilingSchemeMarks(): Promise<FilingSchemeMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników schematu składania", 200)
}

export async function saveFilingSchemeMark(body: FilingSchemeMarkWrite): Promise<FilingSchemeMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika schematu składania", 201)
}
