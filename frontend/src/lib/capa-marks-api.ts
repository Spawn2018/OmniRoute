import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const CAPA_API = "/api/v1/capa-marks"

export type CapaMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  mark_kind: string
  source_ref: string
}

export type CapaMarkWrite = {
  mark_code: string
  mark_kind: string
  source_ref: string
}

export function buildCapaWrite(fields: {
  code: string
  kind: string
  origin: string
}): CapaMarkWrite {
  return {
    mark_code: fields.code.trim(),
    mark_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function capaJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCapaMarks(): Promise<CapaMarkRow[]> {
  const response = await fetch(CAPA_API, { headers: requireAuthHeaders() })
  return capaJson(response, "Błąd listy znaczników CAPA", 200)
}

export async function saveCapaMark(body: CapaMarkWrite): Promise<CapaMarkRow> {
  const response = await fetch(CAPA_API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return capaJson(response, "Błąd zapisu znacznika CAPA", 201)
}
