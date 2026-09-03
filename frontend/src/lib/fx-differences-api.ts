import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FxDifferenceRow = {
  id: string
  organization_id: string
  quotation_id: string
  nbp_rate_id: string
  source_ref: string
}

const FX_URL = "/api/v1/fx-differences"

export async function fetchFxDifferences(): Promise<FxDifferenceRow[]> {
  const response = await fetch(FX_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy różnic"), httpErrorStatus(response))
  }
  return (await response.json()) as FxDifferenceRow[]
}

export async function recordFxDifference(input: {
  quotation_id: string
  nbp_rate_id: string
  source_ref: string
}): Promise<FxDifferenceRow> {
  const response = await fetch(FX_URL, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd zapisu różnicy"), httpErrorStatus(response))
  }
  return (await response.json()) as FxDifferenceRow
}
