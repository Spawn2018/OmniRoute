import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SalesBindMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bind_kind: string
  source_ref: string
}

export type SalesBindMarkWrite = {
  mark_code: string
  bind_kind: string
  source_ref: string
}

const ROOT = "/api/v1/sales-bind-marks" as const

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function buildSalesBindMarkWrite(
  code: string,
  kind: string,
  origin: string,
): SalesBindMarkWrite {
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

export async function fetchSalesBindMarks(): Promise<SalesBindMarkRow[]> {
  const response = await fetch(ROOT, { headers: requireAuthHeaders() })
  return decodeOk(response, "Błąd listy bind korytarza", 200)
}

export async function saveSalesBindMark(payload: SalesBindMarkWrite): Promise<SalesBindMarkRow> {
  const response = await fetch(ROOT, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  return decodeOk(response, "Błąd zapisu bind korytarza", 201)
}
