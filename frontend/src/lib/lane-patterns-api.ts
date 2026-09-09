import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/lane-patterns"

export type CorridorPattern = {
  id: string
  organization_id: string
  origin_unlocode: string
  destination_unlocode: string
  source_ref: string
}

export type CorridorPatternWrite = {
  origin_unlocode: string
  destination_unlocode: string
  source_ref: string
}

export function patternWrite(draft: {
  startStamp: string
  endStamp: string
  originStamp: string
}): CorridorPatternWrite {
  return {
    origin_unlocode: draft.startStamp.trim(),
    destination_unlocode: draft.endStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listCorridorPatterns(): Promise<CorridorPattern[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy wzorców korytarza"), httpErrorStatus(listed))
  }
  return (await listed.json()) as CorridorPattern[]
}

export async function persistPatternMark(payload: CorridorPatternWrite): Promise<CorridorPattern> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu wzorca korytarza"), httpErrorStatus(posted))
  }
  return (await posted.json()) as CorridorPattern
}
