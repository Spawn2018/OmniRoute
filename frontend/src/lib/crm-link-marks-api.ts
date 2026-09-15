import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const ENDPOINT = "/api/v1/crm-link-marks"

export type CrmLinkMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  link_kind: string
  source_ref: string
}

export type CrmLinkMarkWrite = {
  mark_code: string
  link_kind: string
  source_ref: string
}

export function buildCrmLinkMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CrmLinkMarkWrite {
  return {
    mark_code: fields.code.trim(),
    link_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function readJson<T>(response: Response, failLabel: string, want: number): Promise<T> {
  if (response.status !== want) {
    throw new ApiError(await readApiDetail(response, failLabel), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCrmLinkMarks(): Promise<CrmLinkMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  return readJson(response, "Błąd listy powiązań CRM", 200)
}

export async function saveCrmLinkMark(body: CrmLinkMarkWrite): Promise<CrmLinkMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return readJson(response, "Błąd zapisu powiązania CRM", 201)
}
