import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/twin-marks"

export type TwinStamp = {
  id: string
  organization_id: string
  twin_kind: string
  source_ref: string
}

export type TwinStampWrite = {
  twin_kind: string
  source_ref: string
}

export function twinWrite(draft: { kindStamp: string; originStamp: string }): TwinStampWrite {
  return {
    twin_kind: draft.kindStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listTwinMarks(): Promise<TwinStamp[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.ok) {
    return (await listed.json()) as TwinStamp[]
  }
  throw new ApiError(await readApiDetail(listed, "Błąd listy bliźniaków"), httpErrorStatus(listed))
}

export async function persistTwinMark(payload: TwinStampWrite): Promise<TwinStamp> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  const created = posted.ok && posted.status === 201
  if (created) {
    return (await posted.json()) as TwinStamp
  }
  throw new ApiError(await readApiDetail(posted, "Błąd zapisu bliźniaka"), httpErrorStatus(posted))
}
