import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-rounds"

export type TurnMark = {
  id: string
  organization_id: string
  tender_id: string
  round_no: number
  source_ref: string
}

export type TurnMarkWrite = {
  tender_id: string
  round_no: number
  source_ref: string
}

export function roundWrite(draft: {
  boardStamp: string
  turnStamp: string
  originRef: string
}): TurnMarkWrite {
  const parsed = Number.parseInt(draft.turnStamp.trim(), 10)
  return {
    tender_id: draft.boardStamp.trim(),
    round_no: Number.isFinite(parsed) ? parsed : 0,
    source_ref: draft.originRef.trim(),
  }
}

export async function listTurnMarks(): Promise<TurnMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy rund przetargu"), httpErrorStatus(reply))
  }
  return (await reply.json()) as TurnMark[]
}

export async function persistRoundMark(payload: TurnMarkWrite): Promise<TurnMark> {
  const body = JSON.stringify(payload)
  const headers = { ...requireAuthHeaders(), "Content-Type": "application/json" }
  const reply = await fetch(PATH, { method: "POST", headers, body })
  const failed = !reply.ok
  if (failed) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu rundy przetargu"), httpErrorStatus(reply))
  }
  return (await reply.json()) as TurnMark
}
