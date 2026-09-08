import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-lots"

export type LotMark = {
  id: string
  organization_id: string
  tender_id: string
  lot_code: string
  source_ref: string
}

export type LotMarkWrite = {
  tender_id: string
  lot_code: string
  source_ref: string
}

export function lotWrite(draft: {
  boardStamp: string
  codeStamp: string
  originStamp: string
}): LotMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    lot_code: draft.codeStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listLotMarks(): Promise<LotMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy partii przetargu"), httpErrorStatus(reply))
  }
  return (await reply.json()) as LotMark[]
}

export async function persistLotMark(payload: LotMarkWrite): Promise<LotMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.ok) {
    return (await posted.json()) as LotMark
  }
  throw new ApiError(
    await readApiDetail(posted, "Błąd zapisu partii przetargu"),
    httpErrorStatus(posted),
  )
}
