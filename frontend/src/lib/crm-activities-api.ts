import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/crm-activities"

export type CrmActivityRow = {
  id: string
  organization_id: string
  activity_code: string
  activity_kind: string
  source_ref: string
}

export type CrmActivityWrite = {
  activity_code: string
  activity_kind: string
  source_ref: string
}

export function buildCrmActivityWrite(fields: {
  code: string
  kind: string
  origin: string
}): CrmActivityWrite {
  return {
    activity_code: fields.code.trim(),
    activity_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCrmActivities(): Promise<CrmActivityRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy aktywności CRM", 200)
}

export async function saveCrmActivity(
  body: CrmActivityWrite,
): Promise<CrmActivityRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu aktywności CRM", 201)
}
