import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/document-kind-match-marks"

export type DocumentKindMatchMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  match_kind: string
  source_ref: string
}

export type DocumentKindMatchMarkWrite = {
  mark_code: string
  match_kind: string
  source_ref: string
}

export function buildDocumentKindMatchMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): DocumentKindMatchMarkWrite {
  return {
    mark_code: fields.code.trim(),
    match_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchDocumentKindMatchMarks(): Promise<DocumentKindMatchMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow dopasowania rodzaju dokumentu", 200)
}

export async function saveDocumentKindMatchMark(
  body: DocumentKindMatchMarkWrite,
): Promise<DocumentKindMatchMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika dopasowania rodzaju dokumentu", 201)
}
