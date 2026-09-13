import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/crm-opportunities"

export type CrmOpportunityRow = {
  id: string
  organization_id: string
  opportunity_code: string
  stage_kind: string
  source_ref: string
}

export type CrmOpportunityWrite = {
  opportunity_code: string
  stage_kind: string
  source_ref: string
}

export function buildCrmOpportunityWrite(fields: {
  code: string
  kind: string
  origin: string
}): CrmOpportunityWrite {
  return {
    opportunity_code: fields.code.trim(),
    stage_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCrmOpportunities(): Promise<CrmOpportunityRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy okazji CRM", 200)
}

export async function saveCrmOpportunity(
  body: CrmOpportunityWrite,
): Promise<CrmOpportunityRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu okazji CRM", 201)
}
