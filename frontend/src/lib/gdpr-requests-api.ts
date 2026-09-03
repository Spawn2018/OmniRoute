import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type GdprRequestRow = {
  id: string
  organization_id: string
  app_user_id: string
  request_kind: string
  status: string
  source_ref: string
}

const REQUESTS_URL = "/api/v1/gdpr-requests"

export async function fetchGdprRequests(): Promise<GdprRequestRow[]> {
  const response = await fetch(REQUESTS_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy wniosków RODO"), httpErrorStatus(response))
  }
  return (await response.json()) as GdprRequestRow[]
}

export async function recordGdprRequest(input: {
  app_user_id: string
  request_kind: string
  source_ref: string
}): Promise<GdprRequestRow> {
  const response = await fetch(REQUESTS_URL, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd zapisu wniosku RODO"), httpErrorStatus(response))
  }
  return (await response.json()) as GdprRequestRow
}

export async function fulfillGdprRequest(requestId: string): Promise<GdprRequestRow> {
  const response = await fetch(`${REQUESTS_URL}/${requestId}/fulfill`, {
    method: "POST",
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd wypełnienia wniosku RODO"), httpErrorStatus(response))
  }
  return (await response.json()) as GdprRequestRow
}
