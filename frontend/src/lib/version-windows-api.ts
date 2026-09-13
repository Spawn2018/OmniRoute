import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type VersionWindowRow = {
  organization_id: string
  model_version: string
  created_on: string
  pair_count: number
  avg_mae: string
  avg_crps: string
}

const ENDPOINT = "/api/v1/version-windows" as const

export async function loadVersionWindows(): Promise<VersionWindowRow[]> {
  const response = await fetch(ENDPOINT, {
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
    },
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog wyniku okna wersji niedostępny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as VersionWindowRow[]
}
