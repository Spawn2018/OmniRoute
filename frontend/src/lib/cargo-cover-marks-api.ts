import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/cargo-cover-marks"

export type CargoCoverMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  cover_kind: string
  source_ref: string
}

export type CargoCoverMarkWrite = {
  mark_code: string
  cover_kind: string
  source_ref: string
}

export function buildCargoCoverMarkWrite(input: {
  code: string
  kind: string
  origin: string
}): CargoCoverMarkWrite {
  return {
    mark_code: input.code.trim(),
    cover_kind: input.kind.trim().toLowerCase(),
    source_ref: input.origin.trim(),
  }
}

async function readJson<T>(response: Response, message: string, status: number): Promise<T> {
  if (response.status !== status) {
    throw new ApiError(await readApiDetail(response, message), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listCargoCoverMarks(): Promise<CargoCoverMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  return readJson(response, "Nie udało się wczytać cargo cover", 200)
}

export async function saveCargoCoverMark(body: CargoCoverMarkWrite): Promise<CargoCoverMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return readJson(response, "Nie udało się zapisać cargo cover", 201)
}
