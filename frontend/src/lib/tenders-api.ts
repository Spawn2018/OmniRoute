import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tenders"

export type BoardMark = {
  id: string
  organization_id: string
  side: string
  kind: string
  status: string
  buyer_party_id: string
  deadline_at: string
  incoterm: string
  trade_side: string
  named_place: string
  source_ref: string
}

export type BoardMarkWrite = {
  side: string
  kind: string
  status: string
  buyer_party_id: string
  deadline_at: string
  incoterm: string
  trade_side: string
  named_place: string
  source_ref: string
}

export function sideWrite(draft: {
  sideStamp: string
  kindStamp: string
  statusStamp: string
  buyerStamp: string
  untilStamp: string
  termStamp: string
  tradeStamp: string
  placeStamp: string
  originStamp: string
}): BoardMarkWrite {
  return {
    side: draft.sideStamp.trim(),
    kind: draft.kindStamp.trim(),
    status: draft.statusStamp.trim(),
    buyer_party_id: draft.buyerStamp.trim(),
    deadline_at: draft.untilStamp.trim(),
    incoterm: draft.termStamp.trim(),
    trade_side: draft.tradeStamp.trim(),
    named_place: draft.placeStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listBoardMarks(): Promise<BoardMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy przetargów"), httpErrorStatus(reply))
  }
  return (await reply.json()) as BoardMark[]
}

export async function persistSideMark(payload: BoardMarkWrite): Promise<BoardMark> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu przetargu"), httpErrorStatus(reply))
  }
  return (await reply.json()) as BoardMark
}
