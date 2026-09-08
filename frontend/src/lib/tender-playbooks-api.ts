import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-playbooks"

export type PlayMark = {
  id: string
  organization_id: string
  tender_id: string
  claim_code: string
  claim_text: string
  source_ref: string
}

export type PlayMarkWrite = {
  tender_id: string
  claim_code: string
  claim_text: string
  source_ref: string
}

export function playWrite(draft: {
  boardStamp: string
  thesisStamp: string
  bodyStamp: string
  originStamp: string
}): PlayMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    claim_code: draft.thesisStamp.trim(),
    claim_text: draft.bodyStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listPlayMarks(): Promise<PlayMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy playbooka przetargu"),
      httpErrorStatus(listed),
    )
  }
  const pack: unknown = await listed.json()
  return pack as PlayMark[]
}

export async function persistPlayMark(payload: PlayMarkWrite): Promise<PlayMark> {
  const wire = JSON.stringify(payload)
  const posted = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "play-desk",
    },
    body: wire,
  })
  const missed = posted.status !== 201
  if (missed) {
    const why = await readApiDetail(posted, "Błąd zapisu playbooka przetargu")
    throw new ApiError(why, httpErrorStatus(posted))
  }
  const play: unknown = await posted.json()
  return play as PlayMark
}
