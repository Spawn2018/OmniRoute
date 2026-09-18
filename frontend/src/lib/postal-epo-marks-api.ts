import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/postal-epo-marks"

export type PostalEpoMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  epo_kind: string
  source_ref: string
}

export type PostalEpoMarkWrite = {
  mark_code: string
  epo_kind: string
  source_ref: string
}

export function buildPostalEpoMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): PostalEpoMarkWrite {
  return {
    mark_code: fields.code.trim(),
    epo_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchPostalEpoMarks(): Promise<PostalEpoMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow znacznika EPO", 200)
}

export async function savePostalEpoMark(body: PostalEpoMarkWrite): Promise<PostalEpoMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika znacznika EPO", 201)
}
