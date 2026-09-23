import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LocalChargeWarningMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  warning_kind: string
  source_ref: string
}

export type LocalChargeWarningMarkWrite = {
  mark_code: string
  warning_kind: string
  source_ref: string
}

const ROOT = "/api/v1/local-charge-warning-marks" as const

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function buildLocalChargeWarningMarkWrite(
  code: string,
  kind: string,
  origin: string,
): LocalChargeWarningMarkWrite {
  return {
    mark_code: code.trim(),
    warning_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function decodeOk<T>(response: Response, whenFail: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
}

export async function fetchLocalChargeWarningMarks(): Promise<LocalChargeWarningMarkRow[]> {
  const response = await fetch(ROOT, { headers: requireAuthHeaders() })
  return decodeOk(response, "Błąd listy ostrzeżeń dopłaty lokalnej", 200)
}

export async function saveLocalChargeWarningMark(
  payload: LocalChargeWarningMarkWrite,
): Promise<LocalChargeWarningMarkRow> {
  const response = await fetch(ROOT, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  return decodeOk(response, "Błąd zapisu ostrzeżenia dopłaty lokalnej", 201)
}
