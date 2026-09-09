import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-prospects"

export type ProspectMark = {
  id: string
  organization_id: string
  tender_id: string
  party_id: string
  outreach_code: string
  source_ref: string
}

export type ProspectMarkWrite = {
  tender_id: string
  party_id: string
  outreach_code: string
  source_ref: string
}

export function prospectWrite(draft: {
  boardStamp: string
  partyStamp: string
  outreachStamp: string
  originStamp: string
}): ProspectMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    party_id: draft.partyStamp.trim(),
    outreach_code: draft.outreachStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listProspectMarks(): Promise<ProspectMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy prospektów przetargu"),
      httpErrorStatus(listed),
    )
  }
  const pack: unknown = await listed.json()
  return pack as ProspectMark[]
}

export async function persistProspectMark(payload: ProspectMarkWrite): Promise<ProspectMark> {
  const packed = JSON.stringify(payload)
  const posted = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "prospect-desk",
    },
    body: packed,
  })
  const failed = posted.status !== 201
  if (failed) {
    const note = await readApiDetail(posted, "Błąd zapisu prospektu przetargu")
    throw new ApiError(note, httpErrorStatus(posted))
  }
  const mark: unknown = await posted.json()
  return mark as ProspectMark
}
