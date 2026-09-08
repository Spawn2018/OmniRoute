import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type StoredOperatorNotice = {
  id: string
  organization_id: string
  kind: string
  body: string
  status: "unread" | "read"
  read_at: string | null
  source_ref: string
}

export type NoticeDraft = {
  body: string
  sourceRef: string
  kind?: string
}

export const EMPTY_NOTICE_DRAFT: NoticeDraft = {
  body: "",
  sourceRef: "fixture://operator-notice/1",
}

export function operatorNoticeCreateBody(draft: NoticeDraft): {
  body: string
  source_ref: string
  kind?: string
} {
  const payload: { body: string; source_ref: string; kind?: string } = {
    body: draft.body.trim(),
    source_ref: draft.sourceRef.trim(),
  }
  const kind = draft.kind?.trim()
  if (kind !== undefined && kind !== "") {
    payload.kind = kind
  }
  return payload
}

export function noReplyNoticeCreateBody(inquiryId: string): {
  body: string
  source_ref: string
  kind: "no_reply"
} {
  const token = inquiryId.trim()
  return {
    body: `brak odpowiedzi: ${token}`,
    source_ref: `tenant:manual:inquiry:${token}`,
    kind: "no_reply",
  }
}

async function readNotice(response: Response, fallback: string): Promise<StoredOperatorNotice> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as StoredOperatorNotice
}

export async function fetchOperatorNotices(): Promise<StoredOperatorNotice[]> {
  const response = await fetch("/api/v1/operator-notices", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy powiadomień"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as StoredOperatorNotice[]
}

export async function createOperatorNotice(
  body: ReturnType<typeof operatorNoticeCreateBody>,
): Promise<StoredOperatorNotice> {
  const response = await fetch("/api/v1/operator-notices", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readNotice(response, "Błąd zapisu powiadomienia")
}

export async function readOperatorNotice(noticeId: string): Promise<StoredOperatorNotice> {
  const response = await fetch(`/api/v1/operator-notices/${noticeId}/read`, {
    method: "POST",
    headers: requireAuthHeaders(),
  })
  return readNotice(response, "Błąd odczytu powiadomienia")
}
