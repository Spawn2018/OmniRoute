import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/load-plan-marks"

export type LoadPlanMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  stance_kind: string
  source_ref: string
}

export type LoadPlanMarkWrite = {
  mark_code: string
  stance_kind: string
  source_ref: string
}

export function buildLoadPlanMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): LoadPlanMarkWrite {
  return {
    mark_code: fields.code.trim(),
    stance_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchLoadPlanMarks(): Promise<LoadPlanMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników planu załadunku", 200)
}

export async function saveLoadPlanMark(body: LoadPlanMarkWrite): Promise<LoadPlanMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika planu załadunku", 201)
}
