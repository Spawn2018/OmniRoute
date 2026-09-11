import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/cutoff-marks"

export type CutoffMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  cutoff_kind: string
  source_ref: string
}

export type CutoffMarkWrite = {
  mark_code: string
  cutoff_kind: string
  source_ref: string
}

export function buildCutoffMarkWrite(parts: {
  code: string
  kind: string
  origin: string
}): CutoffMarkWrite {
  return {
    mark_code: parts.code.trim(),
    cutoff_kind: parts.kind.trim().toLowerCase(),
    source_ref: parts.origin.trim(),
  }
}

async function load<T>(response: Response, fail: string, ok: number): Promise<T> {
  if (response.status !== ok) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listCutoffMarks(): Promise<CutoffMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  return load(response, "Lista cutoff niedostępna", 200)
}

export async function saveCutoffMark(body: CutoffMarkWrite): Promise<CutoffMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return load(response, "Zapis cutoff nieudany", 201)
}
