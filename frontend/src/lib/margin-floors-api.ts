import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type MarginFloorRow = {
  id: string
  organization_id: string
  floor_code: string
  origin_unlocode: string
  destination_unlocode: string
  floor_amount: string
  floor_currency: string
  source_ref: string
}

export type MarginFloorPayload = {
  floor_code: string
  origin_unlocode: string
  destination_unlocode: string
  floor_amount: string
  floor_currency: string
  source_ref: string
}

const ENDPOINT = "/api/v1/margin-floors" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeMarginFloorPayload(draft: {
  floorCode: string
  originUnlocode: string
  destinationUnlocode: string
  floorAmount: string
  floorCurrency: string
  sourceRef: string
}): MarginFloorPayload {
  return {
    floor_code: draft.floorCode.trim(),
    origin_unlocode: draft.originUnlocode.trim().toUpperCase(),
    destination_unlocode: draft.destinationUnlocode.trim().toUpperCase(),
    floor_amount: draft.floorAmount.trim(),
    floor_currency: draft.floorCurrency.trim().toUpperCase(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadMarginFloors(): Promise<MarginFloorRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog podłogi marży niedostępny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MarginFloorRow[]
}

export async function createMarginFloor(
  payload: MarginFloorPayload,
): Promise<MarginFloorRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "margin-floor-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis podłogi marży odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MarginFloorRow
}
