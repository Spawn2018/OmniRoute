import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/legal-hold-marks"

export type LegalHoldMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  hold_kind: string
  source_ref: string
}

export type LegalHoldMarkWrite = {
  mark_code: string
  hold_kind: string
  source_ref: string
}

export function buildLegalHoldMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): LegalHoldMarkWrite {
  return {
    mark_code: fields.code.trim(),
    hold_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchLegalHoldMarks(): Promise<LegalHoldMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników legal hold", 200)
}

export async function saveLegalHoldMark(body: LegalHoldMarkWrite): Promise<LegalHoldMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika legal hold", 201)
}
