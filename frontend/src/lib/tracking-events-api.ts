import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TrackingEvent = {
  id: string
  organization_id: string
  shipment_id: string
  event_kind: string
  occurred_at: string
  source_ref: string
}

export async function fetchTrackingEvents(): Promise<TrackingEvent[]> {
  const response = await fetch("/api/v1/tracking-events", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy zdarzeń trackingu"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as TrackingEvent[]
}

export async function createTrackingEvent(input: {
  shipment_id: string
  event_kind: string
  occurred_at: string
  source_ref: string
}): Promise<TrackingEvent> {
  const response = await fetch("/api/v1/tracking-events", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu zdarzenia trackingu"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as TrackingEvent
}
