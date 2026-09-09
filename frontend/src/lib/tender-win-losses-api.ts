import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-win-losses"

export type VerdictMark = {
  id: string
  organization_id: string
  tender_id: string
  outcome: string
  reason_code: string
  source_ref: string
}

export type VerdictMarkWrite = {
  tender_id: string
  outcome: string
  reason_code: string
  source_ref: string
}

export function verdictWrite(draft: {
  boardStamp: string
  resultStamp: string
  whyStamp: string
  originStamp: string
}): VerdictMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    outcome: draft.resultStamp.trim(),
    reason_code: draft.whyStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listVerdictMarks(): Promise<VerdictMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(
      await readApiDetail(listed, "Błąd listy wyników przetargu"),
      httpErrorStatus(listed),
    )
  }
  const pack: unknown = await listed.json()
  return pack as VerdictMark[]
}

export async function persistVerdictMark(payload: VerdictMarkWrite): Promise<VerdictMark> {
  const packed = JSON.stringify(payload)
  const posted = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "verdict-desk",
    },
    body: packed,
  })
  const failed = posted.status !== 201
  if (failed) {
    const note = await readApiDetail(posted, "Błąd zapisu wyniku przetargu")
    throw new ApiError(note, httpErrorStatus(posted))
  }
  const verdict: unknown = await posted.json()
  return verdict as VerdictMark
}
