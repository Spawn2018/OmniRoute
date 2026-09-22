import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PalletSynchroMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  synchro_kind: string
  source_ref: string
}

export type PalletSynchroMarkWrite = {
  mark_code: string
  synchro_kind: string
  source_ref: string
}

const ROOT = "/api/v1/pallet-synchro-marks" as const

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    "Content-Type": "application/json",
  }
}

export function buildPalletSynchroMarkWrite(
  code: string,
  kind: string,
  origin: string,
): PalletSynchroMarkWrite {
  return {
    mark_code: code.trim(),
    synchro_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function decodeOk<T>(response: Response, whenFail: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
}

export async function fetchPalletSynchroMarks(): Promise<PalletSynchroMarkRow[]> {
  const response = await fetch(ROOT, { headers: requireAuthHeaders() })
  return decodeOk(response, "Błąd listy synchro palet", 200)
}

export async function savePalletSynchroMark(
  payload: PalletSynchroMarkWrite,
): Promise<PalletSynchroMarkRow> {
  const response = await fetch(ROOT, {
    method: "POST",
    headers: authJsonHeaders(),
    body: JSON.stringify(payload),
  })
  return decodeOk(response, "Błąd zapisu synchro palet", 201)
}
