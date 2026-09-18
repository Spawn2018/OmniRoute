import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/ais-import-marks"

export type AisImportMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  import_kind: string
  source_ref: string
}

export type AisImportMarkWrite = {
  mark_code: string
  import_kind: string
  source_ref: string
}

export function buildAisImportMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): AisImportMarkWrite {
  return {
    mark_code: fields.code.trim(),
    import_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchAisImportMarks(): Promise<AisImportMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow AIS/AES/Intrastat", 200)
}

export async function saveAisImportMark(body: AisImportMarkWrite): Promise<AisImportMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika AIS/AES/Intrastat", 201)
}
