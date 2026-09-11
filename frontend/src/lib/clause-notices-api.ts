import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/clause-notices"

export type ClauseNoticeRow = {
  id: string
  organization_id: string
  notice_code: string
  clause_label: string
  source_ref: string
}

export type ClauseNoticeWrite = {
  notice_code: string
  clause_label: string
  source_ref: string
}

export function buildClauseWrite(fields: {
  code: string
  label: string
  origin: string
}): ClauseNoticeWrite {
  return {
    notice_code: fields.code.trim(),
    clause_label: fields.label.trim(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchClauseNotices(): Promise<ClauseNoticeRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy powiadomień o klauzuli", 200)
}

export async function saveClauseNotice(body: ClauseNoticeWrite): Promise<ClauseNoticeRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu powiadomienia o klauzuli", 201)
}
