import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/working-capital-marks"

export type WorkingCapitalMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  capital_kind: string
  source_ref: string
}

export type WorkingCapitalMarkWrite = {
  mark_code: string
  capital_kind: string
  source_ref: string
}

export function buildWorkingCapitalMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): WorkingCapitalMarkWrite {
  return {
    mark_code: fields.code.trim(),
    capital_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchWorkingCapitalMarks(): Promise<WorkingCapitalMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników yard", 200)
}

export async function saveWorkingCapitalMark(body: WorkingCapitalMarkWrite): Promise<WorkingCapitalMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika working capital", 201)
}
