import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/war-room-marks"

export type RoomStamp = {
  id: string
  organization_id: string
  incident_kind: string
  source_ref: string
}

export type RoomStampWrite = {
  incident_kind: string
  source_ref: string
}

export function roomWrite(draft: { kindStamp: string; originStamp: string }): RoomStampWrite {
  return {
    incident_kind: draft.kindStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listWarRoomMarks(): Promise<RoomStamp[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.ok) {
    return (await listed.json()) as RoomStamp[]
  }
  throw new ApiError(await readApiDetail(listed, "Błąd listy sali kryzysowej"), httpErrorStatus(listed))
}

export async function persistRoomMark(payload: RoomStampWrite): Promise<RoomStamp> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!posted.ok || posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu sali kryzysowej"), httpErrorStatus(posted))
  }
  return (await posted.json()) as RoomStamp
}
