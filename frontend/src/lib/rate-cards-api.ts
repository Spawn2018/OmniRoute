import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/rate-cards"

export type WhenMark = {
  id: string
  organization_id: string
  card_code: string
  applies_when: string
  amount: string
  currency: string
  source_ref: string
}

export type WhenMarkWrite = {
  card_code: string
  applies_when: string
  amount: string
  currency: string
  source_ref: string
}

export function whenWrite(args: {
  codeToken: string
  whenToken: string
  cashMark: string
  ccyMark: string
  originStamp: string
}): WhenMarkWrite {
  return {
    card_code: args.codeToken.trim(),
    applies_when: args.whenToken.trim(),
    amount: args.cashMark.trim(),
    currency: args.ccyMark.trim().toUpperCase(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listWhenMarks(): Promise<WhenMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy kart stawek"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as WhenMark[]
}

export async function persistWhenMark(payload: WhenMarkWrite): Promise<WhenMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "when-mark",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu karty stawek"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as WhenMark
}
