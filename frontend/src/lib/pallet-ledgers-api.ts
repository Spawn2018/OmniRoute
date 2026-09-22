import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/pallet-ledgers"

export type LedgerRow = {
  id: string
  organization_id: string
  party_id: string
  movement_code: string
  pallet_kind: string
  delta_count: number
  source_ref: string
}

export type LedgerWrite = {
  party_id: string
  movement_code: string
  pallet_kind: string
  delta_count: number
  source_ref: string
}

export function ledgerWrite(args: {
  counterpartToken: string
  codeToken: string
  kindToken: string
  deltaToken: string
  originStamp: string
}): LedgerWrite {
  const digits = args.deltaToken.trim()
  const signed = /^-?\d+$/.test(digits) ? Number.parseInt(digits, 10) : Number.NaN
  return {
    party_id: args.counterpartToken.trim(),
    movement_code: args.codeToken.trim(),
    pallet_kind: args.kindToken.trim(),
    delta_count: Number.isNaN(signed) ? 0 : signed,
    source_ref: args.originStamp.trim(),
  }
}

export async function listLedgerRows(): Promise<LedgerRow[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy ruchów palet"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as LedgerRow[]
}

export async function persistLedgerRow(payload: LedgerWrite): Promise<LedgerRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "pallet-ledger",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu ruchu palet"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as LedgerRow
}
