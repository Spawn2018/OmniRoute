import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/prediction-ledgers"

export type LedgerMark = {
  id: string
  organization_id: string
  prediction_kind: string
  horizon_code: string
  interval_low: string
  interval_high: string
  crps: string | null
  mae: string | null
  model_code: string
  source_ref: string
}

export type LedgerMarkWrite = {
  prediction_kind: string
  horizon_code: string
  interval_low: string
  interval_high: string
  model_code: string
  source_ref: string
}

export function ledgerWrite(draft: {
  kindStamp: string
  horizonStamp: string
  lowStamp: string
  highStamp: string
  modelStamp: string
  originStamp: string
}): LedgerMarkWrite {
  return {
    prediction_kind: draft.kindStamp.trim(),
    horizon_code: draft.horizonStamp.trim(),
    interval_low: draft.lowStamp.trim(),
    interval_high: draft.highStamp.trim(),
    model_code: draft.modelStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseLedger<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listLedgerMarks(): Promise<LedgerMark[]> {
  return parseLedger(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy ledgeru predykcji",
    200,
  )
}

export async function persistLedgerMark(payload: LedgerMarkWrite): Promise<LedgerMark> {
  return parseLedger(
    await fetch(PATH, {
      method: "POST",
      headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
    "Błąd zapisu ledgeru predykcji",
    201,
  )
}
