import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/edi-map-marks"

export type EdiMapMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  map_kind: string
  source_ref: string
}

export type EdiMapMarkWrite = {
  mark_code: string
  map_kind: string
  source_ref: string
}

export function buildEdiMapMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): EdiMapMarkWrite {
  return {
    mark_code: fields.code.trim(),
    map_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchEdiMapMarks(): Promise<EdiMapMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników mapy EDI", 200)
}

export async function saveEdiMapMark(body: EdiMapMarkWrite): Promise<EdiMapMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika mapy EDI", 201)
}
