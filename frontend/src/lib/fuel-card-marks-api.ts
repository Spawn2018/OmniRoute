import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FuelCardMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  card_kind: string
  source_ref: string
}

export type FuelCardMarkPayload = {
  mark_code: string
  card_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/fuel-card-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeFuelCardMarkPayload(
  markCode: string,
  cardKind: string,
  sourceRef: string,
): FuelCardMarkPayload {
  return {
    mark_code: markCode.trim(),
    card_kind: cardKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadFuelCardMarks(): Promise<FuelCardMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog fuel card niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FuelCardMarkRow[]
}

export async function createFuelCardMark(
  payload: FuelCardMarkPayload,
): Promise<FuelCardMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "fuel-card-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika fuel card odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as FuelCardMarkRow
}
