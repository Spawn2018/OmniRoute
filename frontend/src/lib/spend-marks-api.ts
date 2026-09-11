import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/spend-marks"

export type SpendMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  leakage_kind: string
  source_ref: string
}

export type SpendMarkWrite = {
  mark_code: string
  leakage_kind: string
  source_ref: string
}

export function buildSpendMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): SpendMarkWrite {
  return {
    mark_code: fields.code.trim(),
    leakage_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchSpendMarks(): Promise<SpendMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników wycieku", 200)
}

export async function saveSpendMark(body: SpendMarkWrite): Promise<SpendMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika wycieku", 201)
}
