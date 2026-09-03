import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type MoneyCostRow = {
  id: string
  organization_id: string
  bank_payment_id: string
  nbp_rate_id: string
  source_ref: string
}

const COST_URL = "/api/v1/money-costs"

export async function fetchMoneyCosts(): Promise<MoneyCostRow[]> {
  const response = await fetch(COST_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy kosztów"), httpErrorStatus(response))
  }
  return (await response.json()) as MoneyCostRow[]
}

export async function recordMoneyCost(input: {
  bank_payment_id: string
  nbp_rate_id: string
  source_ref: string
}): Promise<MoneyCostRow> {
  const response = await fetch(COST_URL, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd zapisu kosztu"), httpErrorStatus(response))
  }
  return (await response.json()) as MoneyCostRow
}
