import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FairShareMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  share_kind: string
  source_ref: string
}

export type FairSharePayload = {
  mark_code: string
  share_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/fair-share-marks"

export function makeFairSharePayload(
  code: string,
  kind: string,
  ref: string,
): FairSharePayload {
  return {
    mark_code: code.trim(),
    share_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadFairShareMarks(): Promise<FairShareMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Lista znacznikow fair share niedostepna"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FairShareMarkRow[]
}

export async function createFairShareMark(
  body: FairSharePayload,
): Promise<FairShareMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika fair share nieudany"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FairShareMarkRow
}
