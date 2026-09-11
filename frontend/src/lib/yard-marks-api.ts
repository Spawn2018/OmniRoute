import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/yard-marks"

export type YardMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  yard_kind: string
  source_ref: string
}

export type YardMarkWrite = {
  mark_code: string
  yard_kind: string
  source_ref: string
}

export function buildYardMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): YardMarkWrite {
  return {
    mark_code: fields.code.trim(),
    yard_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchYardMarks(): Promise<YardMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników yard", 200)
}

export async function saveYardMark(body: YardMarkWrite): Promise<YardMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika yard", 201)
}
