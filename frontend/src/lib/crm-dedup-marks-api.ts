import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/crm-dedup-marks"

export type CrmDedupMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  dedup_kind: string
  source_ref: string
}

export type CrmDedupMarkWrite = {
  mark_code: string
  dedup_kind: string
  source_ref: string
}

export function buildCrmDedupMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CrmDedupMarkWrite {
  const mark_code = fields.code.trim()
  const dedup_kind = fields.kind.trim().toLowerCase()
  const source_ref = fields.origin.trim()
  return { mark_code, dedup_kind, source_ref }
}

async function parseBody<T>(response: Response, failLabel: string, want: number): Promise<T> {
  if (response.status !== want) {
    const detail = await readApiDetail(response, failLabel)
    throw new ApiError(detail, httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCrmDedupMarks(): Promise<CrmDedupMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  return parseBody(response, "Błąd listy stance dedup CRM", 200)
}

export async function saveCrmDedupMark(body: CrmDedupMarkWrite): Promise<CrmDedupMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return parseBody(response, "Błąd zapisu stance dedup CRM", 201)
}
