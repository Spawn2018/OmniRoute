import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PostingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  posting_kind: string
  source_ref: string
}

export type PostingMarkPayload = {
  mark_code: string
  posting_kind: string
  source_ref: string
}

const POSTING_URL = "/api/v1/posting-marks"

export function makePostingMarkPayload(
  markCode: string,
  postingKind: string,
  sourceRef: string,
): PostingMarkPayload {
  return {
    mark_code: markCode.trim(),
    posting_kind: postingKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadPostingMarks(): Promise<PostingMarkRow[]> {
  const res = await fetch(POSTING_URL, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Katalog posting niedostepny"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as PostingMarkRow[]
}

export async function createPostingMark(
  payload: PostingMarkPayload,
): Promise<PostingMarkRow> {
  const res = await fetch(POSTING_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "posting-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis posting odrzucony"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as PostingMarkRow
}
