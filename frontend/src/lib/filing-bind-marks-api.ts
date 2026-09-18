import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/filing-bind-marks"

export type FilingBindMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bind_kind: string
  source_ref: string
}

export type FilingBindMarkWrite = {
  mark_code: string
  bind_kind: string
  source_ref: string
}

export function buildFilingBindMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): FilingBindMarkWrite {
  return {
    mark_code: fields.code.trim(),
    bind_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchFilingBindMarks(): Promise<FilingBindMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow wiazania zgloszenia", 200)
}

export async function saveFilingBindMark(body: FilingBindMarkWrite): Promise<FilingBindMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika wiazania zgloszenia", 201)
}
