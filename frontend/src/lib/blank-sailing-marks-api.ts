import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/blank-sailing-marks"

export type BlankSailingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  sailing_kind: string
  source_ref: string
}

export type BlankSailingMarkWrite = {
  mark_code: string
  sailing_kind: string
  source_ref: string
}

export function buildBlankSailingMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): BlankSailingMarkWrite {
  return {
    mark_code: fields.code.trim(),
    sailing_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchBlankSailingMarks(): Promise<BlankSailingMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow blank sailing", 200)
}

export async function saveBlankSailingMark(
  body: BlankSailingMarkWrite,
): Promise<BlankSailingMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika blank sailing", 201)
}
