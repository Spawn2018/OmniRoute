import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const ENDPOINT = "/api/v1/sanctions-marks"

export type SanctionsMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  list_kind: string
  source_ref: string
}

export type SanctionsMarkWrite = {
  mark_code: string
  list_kind: string
  source_ref: string
}

export function buildSanctionsMarkWrite(parts: {
  code: string
  kind: string
  origin: string
}): SanctionsMarkWrite {
  return {
    mark_code: parts.code.trim(),
    list_kind: parts.kind.trim().toLowerCase(),
    source_ref: parts.origin.trim(),
  }
}

async function decode<T>(response: Response, fail: string, want: number): Promise<T> {
  if (response.status !== want) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listSanctionsMarks(): Promise<SanctionsMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  return decode(response, "Lista sankcji niedostępna", 200)
}

export async function saveSanctionsMark(body: SanctionsMarkWrite): Promise<SanctionsMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return decode(response, "Zapis sankcji nieudany", 201)
}
