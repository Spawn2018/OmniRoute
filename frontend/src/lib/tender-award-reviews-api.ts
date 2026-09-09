import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/tender-award-reviews"

export type AwardReviewMark = {
  id: string
  organization_id: string
  tender_id: string
  review_code: string
  source_ref: string
}

export type AwardReviewMarkWrite = {
  tender_id: string
  review_code: string
  source_ref: string
}

export function awardReviewWrite(draft: {
  boardStamp: string
  reviewStamp: string
  originStamp: string
}): AwardReviewMarkWrite {
  return {
    tender_id: draft.boardStamp.trim(),
    review_code: draft.reviewStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

export async function listAwardReviewMarks(): Promise<AwardReviewMark[]> {
  const listed = await fetch(PATH, { headers: requireAuthHeaders() })
  if (listed.status !== 200) {
    throw new ApiError(await readApiDetail(listed, "Błąd listy przeglądów nagrody"), httpErrorStatus(listed))
  }
  return (await listed.json()) as AwardReviewMark[]
}

export async function persistAwardReviewMark(payload: AwardReviewMarkWrite): Promise<AwardReviewMark> {
  const posted = await fetch(PATH, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (posted.status !== 201) {
    throw new ApiError(await readApiDetail(posted, "Błąd zapisu przeglądu nagrody"), httpErrorStatus(posted))
  }
  return (await posted.json()) as AwardReviewMark
}
