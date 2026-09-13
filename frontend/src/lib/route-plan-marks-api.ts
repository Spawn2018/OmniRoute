import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/route-plan-marks"

export type RoutePlanMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  plan_kind: string
  source_ref: string
}

export type RoutePlanMarkWrite = {
  mark_code: string
  plan_kind: string
  source_ref: string
}

export function buildRoutePlanMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): RoutePlanMarkWrite {
  return {
    mark_code: fields.code.trim(),
    plan_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchRoutePlanMarks(): Promise<RoutePlanMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników planu trasy", 200)
}

export async function saveRoutePlanMark(body: RoutePlanMarkWrite): Promise<RoutePlanMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika planu trasy", 201)
}
