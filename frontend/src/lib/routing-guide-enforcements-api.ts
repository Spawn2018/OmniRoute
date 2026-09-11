import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const ENDPOINT = "/api/v1/routing-guide-enforcements"

export type RoutingGuideEnforcementRow = {
  id: string
  organization_id: string
  mark_code: string
  enforcement_kind: string
  source_ref: string
}

export type EnforcementModeBody = {
  mark_code: string
  enforcement_kind: string
  source_ref: string
}

export function packEnforcementMode(fields: {
  code: string
  mode: string
  origin: string
}): EnforcementModeBody {
  return {
    mark_code: fields.code.trim(),
    enforcement_kind: fields.mode.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function decode<T>(response: Response, fail: string, ok: number): Promise<T> {
  if (response.status !== ok) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchEnforcementModes(): Promise<RoutingGuideEnforcementRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  return decode(response, "Błąd listy trybów egzekucji przewodnika", 200)
}

export async function postEnforcementMode(
  body: EnforcementModeBody,
): Promise<RoutingGuideEnforcementRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return decode(response, "Błąd zapisu trybu egzekucji przewodnika", 201)
}
