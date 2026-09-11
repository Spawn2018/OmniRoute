import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/make-or-buy-marks"

export type MakeOrBuyMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  buy_kind: string
  source_ref: string
}

export type MakeOrBuyMarkWrite = {
  mark_code: string
  buy_kind: string
  source_ref: string
}

export function buildMakeOrBuyMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): MakeOrBuyMarkWrite {
  return {
    mark_code: fields.code.trim(),
    buy_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchMakeOrBuyMarks(): Promise<MakeOrBuyMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników yard", 200)
}

export async function saveMakeOrBuyMark(body: MakeOrBuyMarkWrite): Promise<MakeOrBuyMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika make-or-buy", 201)
}
