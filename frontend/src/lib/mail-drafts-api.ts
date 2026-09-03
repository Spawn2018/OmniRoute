import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type StoredMailDraft = {
  id: string
  organization_id: string
  subject_kind: string
  subject_id: string
  body: string
  status: "draft" | "sent"
  to_address: string | null
  source_ref: string
}

export type MailDraftDispatch = {
  id: string
  status: "sent"
  to_address: string
  mailto: string
  blocks_auto: boolean | null
}

export type MailDraftForm = {
  subjectId: string
  body: string
  sourceRef: string
}

export const EMPTY_MAIL_DRAFT: MailDraftForm = {
  subjectId: "",
  body: "",
  sourceRef: "fixture://mail-draft/1",
}

export function mailDraftCreateBody(draft: MailDraftForm): {
  subject_id: string
  body: string
  source_ref: string
} {
  return {
    subject_id: draft.subjectId.trim(),
    body: draft.body.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export function mailDraftDecisionBody(draftId: string): {
  subject_kind: "mail_draft"
  subject_id: string
  source_ref: string
} {
  return {
    subject_kind: "mail_draft",
    subject_id: draftId,
    source_ref: "fixture://mail-draft/decide",
  }
}

async function readDraft(response: Response, fallback: string): Promise<StoredMailDraft> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as StoredMailDraft
}

export async function fetchMailDrafts(): Promise<StoredMailDraft[]> {
  const response = await fetch("/api/v1/mail-drafts", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy szkiców maila"), httpErrorStatus(response))
  }
  return (await response.json()) as StoredMailDraft[]
}

export async function createMailDraft(
  body: ReturnType<typeof mailDraftCreateBody>,
): Promise<StoredMailDraft> {
  const response = await fetch("/api/v1/mail-drafts", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readDraft(response, "Błąd zapisu szkicu maila")
}

export async function dispatchMailtoMailDraft(
  draftId: string,
  toAddress: string,
): Promise<MailDraftDispatch> {
  const response = await fetch(`/api/v1/mail-drafts/${draftId}/dispatch-mailto`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ to_address: toAddress.trim() }),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd wysyłki mailto"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MailDraftDispatch
}
