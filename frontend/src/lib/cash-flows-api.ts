import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CashFlowRow = {
  id: string
  organization_id: string
  quotation_id: string
  bank_payment_id: string
  source_ref: string
}

const CASH_FLOW_URL = "/api/v1/cash-flows"

export async function fetchCashFlows(): Promise<CashFlowRow[]> {
  const response = await fetch(CASH_FLOW_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy przepływów"), httpErrorStatus(response))
  }
  return (await response.json()) as CashFlowRow[]
}

export async function recordCashFlow(input: {
  quotation_id: string
  bank_payment_id: string
  source_ref: string
}): Promise<CashFlowRow> {
  const response = await fetch(CASH_FLOW_URL, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd zapisu przepływu"), httpErrorStatus(response))
  }
  return (await response.json()) as CashFlowRow
}
