import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/waste-marks"

export type WasteMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  waste_kind: string
  source_ref: string
}

export type WasteMarkWrite = {
  mark_code: string
  waste_kind: string
  source_ref: string
}

export function buildWasteMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): WasteMarkWrite {
  return {
    mark_code: fields.code.trim(),
    waste_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchWasteMarks(): Promise<WasteMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow odpadow", 200)
}

export async function saveWasteMark(body: WasteMarkWrite): Promise<WasteMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika odpadow", 201)
}
