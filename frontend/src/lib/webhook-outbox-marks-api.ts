import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type WebhookOutboxMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  outbox_kind: string
  source_ref: string
}

export type WebhookOutboxPayload = {
  mark_code: string
  outbox_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/webhook-outbox-marks"

export function makeWebhookOutboxPayload(
  code: string,
  kind: string,
  ref: string,
): WebhookOutboxPayload {
  return {
    mark_code: code.trim(),
    outbox_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadWebhookOutboxMarks(): Promise<WebhookOutboxMarkRow[]> {
  const reply = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (reply.ok) {
    return (await reply.json()) as WebhookOutboxMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(reply, "Lista znaczników webhook outbox niedostępna"),
    httpErrorStatus(reply),
  )
}

export async function createWebhookOutboxMark(
  payload: WebhookOutboxPayload,
): Promise<WebhookOutboxMarkRow> {
  const reply = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status === 201) {
    return (await reply.json()) as WebhookOutboxMarkRow
  }
  throw new ApiError(
    await readApiDetail(reply, "Zapis znacznika webhook outbox nieudany"),
    httpErrorStatus(reply),
  )
}
