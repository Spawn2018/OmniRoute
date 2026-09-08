import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/pallet-balances"

export type PoolMark = {
  id: string
  organization_id: string
  party_id: string
  pallet_kind: string
  unit_count: number
  source_ref: string
}

export type PoolMarkWrite = {
  party_id: string
  pallet_kind: string
  unit_count: number
  source_ref: string
}

export function poolWrite(args: {
  counterpartToken: string
  kindToken: string
  countToken: string
  originStamp: string
}): PoolMarkWrite {
  const digits = args.countToken.trim()
  return {
    party_id: args.counterpartToken.trim(),
    pallet_kind: args.kindToken.trim(),
    unit_count: /^\d+$/.test(digits) ? Number.parseInt(digits, 10) : -1,
    source_ref: args.originStamp.trim(),
  }
}

export async function listPoolMarks(): Promise<PoolMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy sald palet"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as PoolMark[]
}

export async function persistPoolMark(payload: PoolMarkWrite): Promise<PoolMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "pool-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu salda palet"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as PoolMark
}
