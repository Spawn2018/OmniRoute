import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/executive-marks"

export type BriefStamp = {
  id: string
  organization_id: string
  question_kind: string
  source_ref: string
}

export type BriefStampWrite = {
  question_kind: string
  source_ref: string
}

export function briefWrite(draft: { askKind: string; originRef: string }): BriefStampWrite {
  return {
    question_kind: draft.askKind.trim(),
    source_ref: draft.originRef.trim(),
  }
}

export async function listExecutiveMarks(): Promise<BriefStamp[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy pytań zarządu"), httpErrorStatus(listed))
  }
  return (await listed.json()) as BriefStamp[]
}

export async function persistBriefMark(payload: BriefStampWrite): Promise<BriefStamp> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!posted.ok) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu pytania zarządu"), httpErrorStatus(posted))
  }
  return (await posted.json()) as BriefStamp
}
