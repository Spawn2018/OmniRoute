import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-data-rooms"

export type RoomMark = {
  id: string
  organization_id: string
  tender_id: string
  nda_mark: string
  source_ref: string
}

export type RoomMarkWrite = {
  tender_id: string
  nda_mark: string
  source_ref: string
}

export function ndaWrite(draft: {
  boardStamp: string
  ndaStamp: string
  originRef: string
}): RoomMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    nda_mark: draft.ndaStamp.trim(),
    source_ref: draft.originRef.trim(),
  }
}

export async function listRoomMarks(): Promise<RoomMark[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy pokoi danych"), httpErrorStatus(reply))
  }
  return (await reply.json()) as RoomMark[]
}

export async function persistRoomMark(payload: RoomMarkWrite): Promise<RoomMark> {
  const encoded = JSON.stringify(payload)
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: encoded,
  })
  if (!posted.ok) {
    const detail = await readApiDetail(posted, "Błąd zapisu pokoju danych")
    throw new ApiError(detail, httpErrorStatus(posted))
  }
  const saved = (await posted.json()) as RoomMark
  return saved
}
