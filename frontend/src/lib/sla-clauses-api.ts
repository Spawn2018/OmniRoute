import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const SLA_API = "/api/v1/sla-clauses"

export type SlaClauseRow = {
  id: string
  organization_id: string
  customer_contract_id: string
  clause_code: string
  metric_kind: string
  threshold_label: string
  source_ref: string
}

export type SlaClauseWrite = {
  customer_contract_id: string
  clause_code: string
  metric_kind: string
  threshold_label: string
  source_ref: string
}

export function buildSlaWrite(fields: {
  contractId: string
  code: string
  kind: string
  threshold: string
  origin: string
}): SlaClauseWrite {
  return {
    customer_contract_id: fields.contractId.trim(),
    clause_code: fields.code.trim(),
    metric_kind: fields.kind.trim().toLowerCase(),
    threshold_label: fields.threshold.trim(),
    source_ref: fields.origin.trim(),
  }
}

async function slaJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchSlaClauses(): Promise<SlaClauseRow[]> {
  const response = await fetch(SLA_API, { headers: requireAuthHeaders() })
  return slaJson(response, "Błąd listy klauzul SLA", 200)
}

export async function saveSlaClause(body: SlaClauseWrite): Promise<SlaClauseRow> {
  const response = await fetch(SLA_API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return slaJson(response, "Błąd zapisu klauzuli SLA", 201)
}
