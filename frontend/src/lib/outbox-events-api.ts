import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OutboxEvent = {
  id: string
  organization_id: string
  event_kind: string
  subject_id: string
  status: string
  source_ref: string
}

export function outboxEventCreateBody(input: {
  subject_id: string
  source_ref: string
}): { subject_id: string; source_ref: string } {
  return {
    subject_id: input.subject_id.trim(),
    source_ref: input.source_ref.trim(),
  }
}

async function readOutboxEvent(response: Response, fallback: string): Promise<OutboxEvent> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as OutboxEvent
}

export async function fetchOutboxEvents(): Promise<OutboxEvent[]> {
  const response = await fetch("/api/v1/outbox-events", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy outbox"), httpErrorStatus(response))
  }
  return (await response.json()) as OutboxEvent[]
}

export async function recordOutboxEvent(body: {
  subject_id: string
  source_ref: string
}): Promise<OutboxEvent> {
  const response = await fetch("/api/v1/outbox-events", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readOutboxEvent(response, "Błąd zapisu outbox")
}
