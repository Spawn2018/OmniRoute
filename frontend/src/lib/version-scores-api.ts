import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type VersionScoreRow = {
  organization_id: string
  model_version: string
  pair_count: number
  avg_mae: string
  avg_crps: string
}

const ENDPOINT = "/api/v1/version-scores" as const

export async function loadVersionScores(): Promise<VersionScoreRow[]> {
  const response = await fetch(ENDPOINT, {
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
    },
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog wyniku wersji niedostępny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as VersionScoreRow[]
}
