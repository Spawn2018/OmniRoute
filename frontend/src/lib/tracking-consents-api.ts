import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/tracking-consents"

export type TrackingConsentRow = {
  id: string
  organization_id: string
  consent_code: string
  consent_kind: string
  source_ref: string
}

export type TrackingConsentWrite = {
  consent_code: string
  consent_kind: string
  source_ref: string
}

export function buildTrackingConsentWrite(fields: {
  code: string
  kind: string
  origin: string
}): TrackingConsentWrite {
  return {
    consent_code: fields.code.trim(),
    consent_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchTrackingConsents(): Promise<TrackingConsentRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy zgód na śledzenie", 200)
}

export async function saveTrackingConsent(
  body: TrackingConsentWrite,
): Promise<TrackingConsentRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu zgody na śledzenie", 201)
}
