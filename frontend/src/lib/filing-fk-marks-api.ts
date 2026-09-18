import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/filing-fk-marks"

export type FilingFkMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  fk_kind: string
  source_ref: string
}

export type FilingFkMarkWrite = {
  mark_code: string
  fk_kind: string
  source_ref: string
}

export function buildFilingFkMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): FilingFkMarkWrite {
  return {
    mark_code: fields.code.trim(),
    fk_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchFilingFkMarks(): Promise<FilingFkMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy celow FK zgloszenia", 200)
}

export async function saveFilingFkMark(body: FilingFkMarkWrite): Promise<FilingFkMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu celu FK zgloszenia", 201)
}
