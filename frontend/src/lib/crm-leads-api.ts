import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/crm-leads"

export type CrmLeadRow = {
  id: string
  organization_id: string
  lead_code: string
  stage_kind: string
  source_ref: string
}

export type CrmLeadWrite = {
  lead_code: string
  stage_kind: string
  source_ref: string
}

export function buildCrmLeadWrite(fields: {
  code: string
  kind: string
  origin: string
}): CrmLeadWrite {
  return {
    lead_code: fields.code.trim(),
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

export async function fetchCrmLeads(): Promise<CrmLeadRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy leadów CRM", 200)
}

export async function saveCrmLead(body: CrmLeadWrite): Promise<CrmLeadRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu leada CRM", 201)
}
