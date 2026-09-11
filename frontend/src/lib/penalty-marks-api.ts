import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/penalty-marks"

export type PenaltyMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  breach_kind: string
  source_ref: string
}

export type PenaltyMarkWrite = {
  mark_code: string
  breach_kind: string
  source_ref: string
}

export function buildPenaltyMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): PenaltyMarkWrite {
  return {
    mark_code: fields.code.trim(),
    breach_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchPenaltyMarks(): Promise<PenaltyMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników kary", 200)
}

export async function savePenaltyMark(body: PenaltyMarkWrite): Promise<PenaltyMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika kary", 201)
}
