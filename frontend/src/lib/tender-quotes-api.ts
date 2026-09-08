import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-quotes"

export type BidMark = {
  id: string
  organization_id: string
  quotation_id: string
  valid_until: string
  order_limit: number
  source_ref: string
}

export type BidMarkWrite = {
  quotation_id: string
  valid_until: string
  order_limit: number
  source_ref: string
}

export function capWrite(draft: {
  quoteStamp: string
  untilStamp: string
  capCount: string
  originStamp: string
}): BidMarkWrite {
  const digits = draft.capCount.trim()
  return {
    quotation_id: draft.quoteStamp.trim(),
    valid_until: draft.untilStamp.trim(),
    order_limit: /^\d+$/.test(digits) ? Number.parseInt(digits, 10) : 0,
    source_ref: draft.originStamp.trim(),
  }
}

export async function listBidMarks(): Promise<BidMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy ofert przetargowych"), httpErrorStatus(reply))
  }
  return (await reply.json()) as BidMark[]
}

export async function persistCapMark(payload: BidMarkWrite): Promise<BidMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu oferty przetargowej"), httpErrorStatus(reply))
  }
  return (await reply.json()) as BidMark
}
