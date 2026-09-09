import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/local-charges"

export type LevyMark = {
  id: string
  organization_id: string
  charge_kind: string
  amount: string
  currency: string
  port_unlocode: string | null
  iso_size_type: string | null
  source_ref: string
}

export type LevyMarkWrite = {
  charge_kind: string
  amount: string
  currency: string
  source_ref: string
  port_unlocode?: string
  iso_size_type?: string
}

export function levyWrite(args: {
  kindToken: string
  cashMark: string
  ccyMark: string
  originStamp: string
  portToken: string
  isoToken: string
}): LevyMarkWrite {
  const port = args.portToken.trim().toUpperCase()
  const iso = args.isoToken.trim().toUpperCase()
  const body: LevyMarkWrite = {
    charge_kind: args.kindToken.trim().toLowerCase(),
    amount: args.cashMark.trim(),
    currency: args.ccyMark.trim().toUpperCase(),
    source_ref: args.originStamp.trim(),
  }
  if (port !== "") {
    body.port_unlocode = port
  }
  if (iso !== "") {
    body.iso_size_type = iso
  }
  return body
}

export async function listLevyMarks(): Promise<LevyMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy dopłat lokalnych"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as LevyMark[]
}

export async function persistLevyMark(payload: LevyMarkWrite): Promise<LevyMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "levy-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu dopłaty lokalnej"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as LevyMark
}
