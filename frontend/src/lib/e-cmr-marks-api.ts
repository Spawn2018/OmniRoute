import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/e-cmr-marks"

export type ECmrMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  cmr_kind: string
  source_ref: string
}

export type ECmrWrite = {
  mark_code: string
  cmr_kind: string
  source_ref: string
}

export function packECmrWrite(
  code: string,
  kind: string,
  origin: string,
): ECmrWrite {
  return {
    mark_code: code.trim(),
    cmr_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function loadJson<T>(res: Response, fail: string, ok: number): Promise<T> {
  if (res.status === ok) {
    return (await res.json()) as T
  }
  throw new ApiError(await readApiDetail(res, fail), httpErrorStatus(res))
}

export async function listECmrMarks(): Promise<ECmrMarkRow[]> {
  const res = await fetch(PATH, { headers: requireAuthHeaders() })
  return loadJson(res, "Lista znaczników e-cmr niedostępna", 200)
}

export async function saveECmrMark(body: ECmrWrite): Promise<ECmrMarkRow> {
  const res = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return loadJson(res, "Zapis znacznika e-cmr nieudany", 201)
}
