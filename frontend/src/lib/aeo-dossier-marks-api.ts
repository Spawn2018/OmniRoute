import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/aeo-dossier-marks"

export type AeoDossierMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  dossier_kind: string
  source_ref: string
}

export type AeoDossierMarkWrite = {
  mark_code: string
  dossier_kind: string
  source_ref: string
}

export function buildAeoDossierMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): AeoDossierMarkWrite {
  return {
    mark_code: fields.code.trim(),
    dossier_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchAeoDossierMarks(): Promise<AeoDossierMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników dossier AEO", 200)
}

export async function saveAeoDossierMark(body: AeoDossierMarkWrite): Promise<AeoDossierMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika dossier AEO", 201)
}
