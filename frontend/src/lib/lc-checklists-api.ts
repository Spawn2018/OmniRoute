import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/lc-checklists"

export type LcChecklistRow = {
  id: string
  organization_id: string
  checklist_code: string
  status_kind: string
  source_ref: string
}

export type LcChecklistWrite = {
  checklist_code: string
  status_kind: string
  source_ref: string
}

export function buildLcChecklistWrite(fields: {
  code: string
  kind: string
  origin: string
}): LcChecklistWrite {
  return {
    checklist_code: fields.code.trim(),
    status_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchLcChecklists(): Promise<LcChecklistRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy checklist LC", 200)
}

export async function saveLcChecklist(body: LcChecklistWrite): Promise<LcChecklistRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu checklisty LC", 201)
}
