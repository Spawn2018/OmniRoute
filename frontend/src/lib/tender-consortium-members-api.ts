import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-consortium-members"

export type SeatMark = {
  id: string
  organization_id: string
  tender_id: string
  party_id: string
  seat_code: string
  source_ref: string
}

export type SeatMarkWrite = {
  tender_id: string
  party_id: string
  seat_code: string
  source_ref: string
}

export function seatWrite(draft: {
  boardStamp: string
  partyStamp: string
  chairStamp: string
  originStamp: string
}): SeatMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    party_id: draft.partyStamp.trim(),
    seat_code: draft.chairStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listSeatMarks(): Promise<SeatMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy foteli konsorcjum"),
      httpErrorStatus(listed),
    )
  }
  const pack: unknown = await listed.json()
  return pack as SeatMark[]
}

export async function persistSeatMark(payload: SeatMarkWrite): Promise<SeatMark> {
  const packed = JSON.stringify(payload)
  const posted = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "seat-desk",
    },
    body: packed,
  })
  const failed = posted.status !== 201
  if (failed) {
    const note = await readApiDetail(posted, "Błąd zapisu fotela konsorcjum")
    throw new ApiError(note, httpErrorStatus(posted))
  }
  const seat: unknown = await posted.json()
  return seat as SeatMark
}
