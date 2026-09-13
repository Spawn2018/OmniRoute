import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type IntervalScoreRow = {
  organization_id: string
  outcome_id: string
  suggestion_id: string
  entity_id: string
  interval_low: string
  interval_high: string
  actual_value: string
  mae: string
  crps: string
}

const ENDPOINT = "/api/v1/interval-scores" as const

export async function loadIntervalScores(): Promise<IntervalScoreRow[]> {
  const response = await fetch(ENDPOINT, {
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
    },
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog wyniku przedziału niedostępny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as IntervalScoreRow[]
}
