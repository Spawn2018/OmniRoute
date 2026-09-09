import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/rank-marks"

export type AxisStamp = {
  id: string
  organization_id: string
  rank_kind: string
  source_ref: string
}

export type AxisStampWrite = {
  rank_kind: string
  source_ref: string
}

export function rankWrite(draft: { axis: string; origin: string }): AxisStampWrite {
  return {
    rank_kind: draft.axis.trim(),
    source_ref: draft.origin.trim(),
  }
}

export async function listRankMarks(): Promise<AxisStamp[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status === 200) {
    return (await listed.json()) as AxisStamp[]
  }
  throw new ApiError(await readApiDetail(listed, "Błąd listy osi rankingu"), httpErrorStatus(listed))
}

export async function persistRankMark(payload: AxisStampWrite): Promise<AxisStamp> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.ok && posted.status === 201) {
    return (await posted.json()) as AxisStamp
  }
  throw new ApiError(await readApiDetail(posted, "Błąd zapisu osi rankingu"), httpErrorStatus(posted))
}
