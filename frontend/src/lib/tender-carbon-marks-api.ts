import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-carbon-marks"

export type CarbonMark = {
  id: string
  organization_id: string
  tender_id: string
  mark_code: string
  source_ref: string
}

export type CarbonMarkWrite = {
  tender_id: string
  mark_code: string
  source_ref: string
}

export function carbonWrite(draft: {
  boardStamp: string
  markStamp: string
  originStamp: string
}): CarbonMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    mark_code: draft.markStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listCarbonMarks(): Promise<CarbonMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy znaczników śladu"), httpErrorStatus(listed))
  }
  return (await listed.json()) as CarbonMark[]
}

export async function persistCarbonMark(payload: CarbonMarkWrite): Promise<CarbonMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu znacznika śladu"), httpErrorStatus(posted))
  }
  return (await posted.json()) as CarbonMark
}
