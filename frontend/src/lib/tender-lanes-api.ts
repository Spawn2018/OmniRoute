import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-lanes"

export type LaneMark = {
  id: string
  organization_id: string
  tender_lot_id: string
  origin_unlocode: string
  destination_unlocode: string
  source_ref: string
}

export type LaneMarkWrite = {
  tender_lot_id: string
  origin_unlocode: string
  destination_unlocode: string
  source_ref: string
}

export function laneWrite(draft: {
  lotStamp: string
  originStamp: string
  destStamp: string
  originRef: string
}): LaneMarkWrite {
  return {
    tender_lot_id: draft.lotStamp.trim(),
    origin_unlocode: draft.originStamp.trim(),
    destination_unlocode: draft.destStamp.trim(),
    source_ref: draft.originRef.trim(),
  }
}

export async function listLaneMarks(): Promise<LaneMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy korytarzy przetargu"), httpErrorStatus(reply))
  }
  return (await reply.json()) as LaneMark[]
}

export async function persistLaneMark(payload: LaneMarkWrite): Promise<LaneMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.ok) {
    return (await posted.json()) as LaneMark
  }
  throw new ApiError(
    await readApiDetail(posted, "Błąd zapisu korytarza przetargu"),
    httpErrorStatus(posted),
  )
}
