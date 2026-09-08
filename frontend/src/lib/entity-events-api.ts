import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type EntityEvent = {
  id: string
  organization_id: string
  subject_kind: string
  subject_id: string
  event_kind: string
  occurred_at: string
  source_ref: string
}

export function entityEventCreateBody(input: {
  subject_kind: string
  subject_id: string
  event_kind: string
  source_ref: string
}): {
  subject_kind: string
  subject_id: string
  event_kind: string
  source_ref: string
} {
  return {
    subject_kind: input.subject_kind.trim(),
    subject_id: input.subject_id.trim(),
    event_kind: input.event_kind.trim(),
    source_ref: input.source_ref.trim(),
  }
}

async function readEntityEvent(response: Response, fallback: string): Promise<EntityEvent> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as EntityEvent
}

export async function fetchEntityEvents(): Promise<EntityEvent[]> {
  const response = await fetch("/api/v1/entity-events", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy zdarzeń podmiotu"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as EntityEvent[]
}

export async function recordEntityEvent(body: {
  subject_kind: string
  subject_id: string
  event_kind: string
  source_ref: string
}): Promise<EntityEvent> {
  const response = await fetch("/api/v1/entity-events", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readEntityEvent(response, "Błąd zapisu zdarzenia podmiotu")
}
