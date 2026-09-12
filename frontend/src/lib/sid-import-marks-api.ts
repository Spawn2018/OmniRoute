import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SidImportMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  sid_kind: string
  source_ref: string
}

export type SidImportPayload = {
  mark_code: string
  sid_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/sid-import-marks"

export function makeSidImportPayload(
  code: string,
  kind: string,
  ref: string,
): SidImportPayload {
  return {
    mark_code: code.trim(),
    sid_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadSidImportMarks(): Promise<SidImportMarkRow[]> {
  const res = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (res.ok) {
    return (await res.json()) as SidImportMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(res, "Lista znaczników SID niedostępna"),
    httpErrorStatus(res),
  )
}

export async function createSidImportMark(
  payload: SidImportPayload,
): Promise<SidImportMarkRow> {
  const res = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (res.status === 201) {
    return (await res.json()) as SidImportMarkRow
  }
  throw new ApiError(
    await readApiDetail(res, "Zapis znacznika SID nieudany"),
    httpErrorStatus(res),
  )
}
