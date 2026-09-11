import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/cmms-marks"

export type CmmsMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  work_kind: string
  source_ref: string
}

export type CmmsMarkWrite = {
  mark_code: string
  work_kind: string
  source_ref: string
}

export function buildCmmsMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CmmsMarkWrite {
  return {
    mark_code: fields.code.trim(),
    work_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCmmsMarks(): Promise<CmmsMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników CMMS", 200)
}

export async function saveCmmsMark(body: CmmsMarkWrite): Promise<CmmsMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika CMMS", 201)
}
