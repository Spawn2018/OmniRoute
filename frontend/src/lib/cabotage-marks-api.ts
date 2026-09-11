import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CabotageMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  cabotage_kind: string
  source_ref: string
}

type CabotagePayload = {
  mark_code: string
  cabotage_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/cabotage-marks"

export function toCabotagePayload(
  markCode: string,
  kind: string,
  sourceRef: string,
): CabotagePayload {
  return {
    mark_code: markCode.trim(),
    cabotage_kind: kind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

async function parseBody<T>(res: Response, whenFail: string, ok: number): Promise<T> {
  if (res.status === ok) {
    return (await res.json()) as T
  }
  throw new ApiError(await readApiDetail(res, whenFail), httpErrorStatus(res))
}

export async function loadCabotageMarks(): Promise<CabotageMarkRow[]> {
  const res = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  return parseBody(res, "Lista kabotażu niedostępna", 200)
}

export async function createCabotageMark(payload: CabotagePayload): Promise<CabotageMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return parseBody(res, "Zapis kabotażu nieudany", 201)
}
