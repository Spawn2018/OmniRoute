import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type MailAcceptMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  accept_kind: string
  source_ref: string
}

export type MailAcceptMarkPayload = {
  mark_code: string
  accept_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/mail-accept-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeMailAcceptMarkPayload(
  markCode: string,
  acceptKind: string,
  sourceRef: string,
): MailAcceptMarkPayload {
  return {
    mark_code: markCode.trim(),
    accept_kind: acceptKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadMailAcceptMarks(): Promise<MailAcceptMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog Accept z maila niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MailAcceptMarkRow[]
}

export async function createMailAcceptMark(
  payload: MailAcceptMarkPayload,
): Promise<MailAcceptMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "mail-accept-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis Accept z maila odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MailAcceptMarkRow
}
