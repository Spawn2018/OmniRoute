import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/create-block-marks"

export type CreateBlockMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  block_kind: string
  source_ref: string
}

export type CreateBlockMarkWrite = {
  mark_code: string
  block_kind: string
  source_ref: string
}

export function buildCreateBlockMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CreateBlockMarkWrite {
  return {
    mark_code: fields.code.trim(),
    block_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCreateBlockMarks(): Promise<CreateBlockMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow bramy create", 200)
}

export async function saveCreateBlockMark(
  body: CreateBlockMarkWrite,
): Promise<CreateBlockMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika bramy create", 201)
}
