import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/position-events"

export type PositionEventRow = {
  id: string
  organization_id: string
  event_code: string
  source_kind: string
  source_ref: string
}

export type PositionEventWrite = {
  event_code: string
  source_kind: string
  source_ref: string
}

export function buildPositionEventWrite(fields: {
  code: string
  kind: string
  origin: string
}): PositionEventWrite {
  return {
    event_code: fields.code.trim(),
    source_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchPositionEvents(): Promise<PositionEventRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy zdarzeń pozycji", 200)
}

export async function savePositionEvent(
  body: PositionEventWrite,
): Promise<PositionEventRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu zdarzenia pozycji", 201)
}
