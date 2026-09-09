import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-bid-stances"

export type StanceMark = {
  id: string
  organization_id: string
  tender_id: string
  stance_code: string
  source_ref: string
}

export type StanceMarkWrite = {
  tender_id: string
  stance_code: string
  source_ref: string
}

export function stanceWrite(draft: {
  boardStamp: string
  stanceStamp: string
  originStamp: string
}): StanceMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    stance_code: draft.stanceStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listStanceMarks(): Promise<StanceMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy postaw udziału"), httpErrorStatus(listed))
  }
  return (await listed.json()) as StanceMark[]
}

export async function persistStanceMark(payload: StanceMarkWrite): Promise<StanceMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu postawy udziału"), httpErrorStatus(posted))
  }
  return (await posted.json()) as StanceMark
}
