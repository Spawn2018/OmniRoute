import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-ted-notices"

export type TedMark = {
  id: string
  organization_id: string
  tender_id: string
  notice_number: string
  source_ref: string
}

export type TedMarkWrite = {
  tender_id: string
  notice_number: string
  source_ref: string
}

export function tedWrite(draft: {
  boardStamp: string
  noticeStamp: string
  originStamp: string
}): TedMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    notice_number: draft.noticeStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listTedMarks(): Promise<TedMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy ogłoszeń TED"), httpErrorStatus(listed))
  }
  return (await listed.json()) as TedMark[]
}

export async function persistTedMark(payload: TedMarkWrite): Promise<TedMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu ogłoszenia TED"), httpErrorStatus(posted))
  }
  return (await posted.json()) as TedMark
}
