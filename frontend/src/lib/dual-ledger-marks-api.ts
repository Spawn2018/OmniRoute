import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DualLedgerMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  ledger_kind: string
  source_ref: string
}

export type DualLedgerMarkPayload = {
  mark_code: string
  ledger_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/dual-ledger-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeDualLedgerMarkPayload(
  markCode: string,
  ledgerKind: string,
  sourceRef: string,
): DualLedgerMarkPayload {
  return {
    mark_code: markCode.trim(),
    ledger_kind: ledgerKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadDualLedgerMarks(): Promise<DualLedgerMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog dual ledger niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DualLedgerMarkRow[]
}

export async function createDualLedgerMark(
  payload: DualLedgerMarkPayload,
): Promise<DualLedgerMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "dual-ledger-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika dual ledger odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DualLedgerMarkRow
}
