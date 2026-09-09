import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/kreptd-licences"

export type KreptdMark = {
  id: string
  organization_id: string
  party_id: string
  licence_no: string
  source_ref: string
}

export type KreptdMarkWrite = {
  party_id: string
  licence_no: string
  source_ref: string
}

export function kreptdWrite(draft: {
  partyStamp: string
  licenceStamp: string
  originStamp: string
}): KreptdMarkWrite {
  return {
    party_id: draft.partyStamp.trim(),
    licence_no: draft.licenceStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listKreptdMarks(): Promise<KreptdMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy licencji KREPTD"), httpErrorStatus(listed))
  }
  return (await listed.json()) as KreptdMark[]
}

export async function persistKreptdMark(payload: KreptdMarkWrite): Promise<KreptdMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu licencji KREPTD"), httpErrorStatus(posted))
  }
  return (await posted.json()) as KreptdMark
}
