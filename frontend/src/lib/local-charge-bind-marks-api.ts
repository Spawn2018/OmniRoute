import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LocalChargeBindMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bind_kind: string
  source_ref: string
}

export type LocalChargeBindMarkWrite = {
  mark_code: string
  bind_kind: string
  source_ref: string
}

const ROOT = "/api/v1/local-charge-bind-marks" as const

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function buildLocalChargeBindMarkWrite(
  code: string,
  kind: string,
  origin: string,
): LocalChargeBindMarkWrite {
  return {
    mark_code: code.trim(),
    bind_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function decodeOk<T>(response: Response, whenFail: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
}

export async function fetchLocalChargeBindMarks(): Promise<LocalChargeBindMarkRow[]> {
  const response = await fetch(ROOT, { headers: requireAuthHeaders() })
  return decodeOk(response, "Błąd listy wiązań dopłaty lokalnej", 200)
}

export async function saveLocalChargeBindMark(
  payload: LocalChargeBindMarkWrite,
): Promise<LocalChargeBindMarkRow> {
  const response = await fetch(ROOT, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  return decodeOk(response, "Błąd zapisu wiązania dopłaty lokalnej", 201)
}
