import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/postal-dispatch-marks"

export type PostalDispatchMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  dispatch_kind: string
  source_ref: string
}

export type PostalDispatchMarkWrite = {
  mark_code: string
  dispatch_kind: string
  source_ref: string
}

export function buildPostalDispatchMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): PostalDispatchMarkWrite {
  return {
    mark_code: fields.code.trim(),
    dispatch_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchPostalDispatchMarks(): Promise<PostalDispatchMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow ksiazki PP", 200)
}

export async function savePostalDispatchMark(
  body: PostalDispatchMarkWrite,
): Promise<PostalDispatchMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika ksiazki PP", 201)
}
