import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/party-documents"

export type PartyDocMark = {
  id: string
  organization_id: string
  party_id: string
  document_kind: string
  source_ref: string
}

export type PartyDocMarkWrite = {
  party_id: string
  document_kind: string
  source_ref: string
}

export function partyDocWrite(draft: {
  partyStamp: string
  kindStamp: string
  originStamp: string
}): PartyDocMarkWrite {
  return {
    party_id: draft.partyStamp.trim(),
    document_kind: draft.kindStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listPartyDocMarks(): Promise<PartyDocMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy dokumentów kontrahenta"),
      httpErrorStatus(listed),
    )
  }
  return (await listed.json()) as PartyDocMark[]
}

export async function persistPartyDocMark(payload: PartyDocMarkWrite): Promise<PartyDocMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(
      await readApiDetail(posted, "Błąd zapisu dokumentu kontrahenta"),
      httpErrorStatus(posted),
    )
  }
  return (await posted.json()) as PartyDocMark
}
