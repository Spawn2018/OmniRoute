import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const MARK_PATH = "/api/v1/otif-marks"

export type OtifMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  scope_kind: string
  source_ref: string
}

export type OtifMarkBody = {
  mark_code: string
  scope_kind: string
  source_ref: string
}

export function otifMarkBody(draft: {
  markSlug: string
  scopeKind: string
  originPointer: string
}): OtifMarkBody {
  return {
    mark_code: draft.markSlug.trim(),
    scope_kind: draft.scopeKind.trim().toLowerCase(),
    source_ref: draft.originPointer.trim(),
  }
}

async function readMarkJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listOtifMarks(): Promise<OtifMarkRow[]> {
  const listed = await fetch(MARK_PATH, { headers: requireAuthHeaders() })
  return readMarkJson(listed, "Błąd listy znaczników OTIF", 200)
}

export async function persistOtifMark(payload: OtifMarkBody): Promise<OtifMarkRow> {
  const posted = await fetch(MARK_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readMarkJson(posted, "Błąd zapisu znacznika OTIF", 201)
}
