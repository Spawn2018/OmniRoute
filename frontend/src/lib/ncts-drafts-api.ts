import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/ncts-drafts"

export type NctsDraftRow = {
  id: string
  organization_id: string
  draft_code: string
  transit_kind: string
  source_ref: string
}

export type NctsDraftWrite = {
  draft_code: string
  transit_kind: string
  source_ref: string
}

export function buildNctsDraftWrite(fields: {
  code: string
  kind: string
  origin: string
}): NctsDraftWrite {
  return {
    draft_code: fields.code.trim(),
    transit_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchNctsDrafts(): Promise<NctsDraftRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy szkiców NCTS", 200)
}

export async function saveNctsDraft(body: NctsDraftWrite): Promise<NctsDraftRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu szkicu NCTS", 201)
}
