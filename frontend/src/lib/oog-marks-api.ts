import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/oog-marks"

export type OogMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  escort_kind: string
  source_ref: string
}

export type OogMarkWrite = {
  mark_code: string
  escort_kind: string
  source_ref: string
}

export function buildOogMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): OogMarkWrite {
  return {
    mark_code: fields.code.trim(),
    escort_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchOogMarks(): Promise<OogMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników OOG", 200)
}

export async function saveOogMark(body: OogMarkWrite): Promise<OogMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika OOG", 201)
}
