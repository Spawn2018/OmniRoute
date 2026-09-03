import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CostToServeRow = {
  id: string
  organization_id: string
  customer_sop_id: string
  quotation_id: string
  source_ref: string
}

const COST_URL = "/api/v1/cost-to-serves"

export async function fetchCostToServeRows(): Promise<CostToServeRow[]> {
  const response = await fetch(COST_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy kosztu obsługi"), httpErrorStatus(response))
  }
  return (await response.json()) as CostToServeRow[]
}

export async function recordCostToServe(input: {
  customer_sop_id: string
  quotation_id: string
  source_ref: string
}): Promise<CostToServeRow> {
  const response = await fetch(COST_URL, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd zapisu kosztu obsługi"), httpErrorStatus(response))
  }
  return (await response.json()) as CostToServeRow
}
