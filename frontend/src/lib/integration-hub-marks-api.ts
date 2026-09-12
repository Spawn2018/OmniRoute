import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type IntegrationHubMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  hub_kind: string
  source_ref: string
}

export type IntegrationHubPayload = {
  mark_code: string
  hub_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/integration-hub-marks"

export function makeIntegrationHubPayload(
  code: string,
  kind: string,
  ref: string,
): IntegrationHubPayload {
  return {
    mark_code: code.trim(),
    hub_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadIntegrationHubMarks(): Promise<IntegrationHubMarkRow[]> {
  const response = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (response.ok) {
    return (await response.json()) as IntegrationHubMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(response, "Lista protokołów hubu niedostępna"),
    httpErrorStatus(response),
  )
}

export async function createIntegrationHubMark(
  payload: IntegrationHubPayload,
): Promise<IntegrationHubMarkRow> {
  const response = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (response.status === 201) {
    return (await response.json()) as IntegrationHubMarkRow
  }
  throw new ApiError(
    await readApiDetail(response, "Zapis protokołu hubu nieudany"),
    httpErrorStatus(response),
  )
}
