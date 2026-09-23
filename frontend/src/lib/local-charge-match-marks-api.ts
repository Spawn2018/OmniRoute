import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LocalChargeMatchMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  match_kind: string
  source_ref: string
}

export type LocalChargeMatchMarkWrite = {
  mark_code: string
  match_kind: string
  source_ref: string
}

const ROOT = "/api/v1/local-charge-match-marks" as const

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function buildLocalChargeMatchMarkWrite(
  code: string,
  kind: string,
  origin: string,
): LocalChargeMatchMarkWrite {
  return {
    mark_code: code.trim(),
    match_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function decodeOk<T>(response: Response, whenFail: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
}

export async function fetchLocalChargeMatchMarks(): Promise<LocalChargeMatchMarkRow[]> {
  const response = await fetch(ROOT, { headers: requireAuthHeaders() })
  return decodeOk(response, "Błąd listy wiązań przekazania", 200)
}

export async function saveLocalChargeMatchMark(
  payload: LocalChargeMatchMarkWrite,
): Promise<LocalChargeMatchMarkRow> {
  const response = await fetch(ROOT, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  return decodeOk(response, "Błąd zapisu dopasowania dopłaty lokalnej", 201)
}
