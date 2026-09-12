import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SpotContractMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  deal_kind: string
  source_ref: string
}

export type SpotContractMarkPayload = {
  mark_code: string
  deal_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/spot-contract-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeSpotContractMarkPayload(
  markCode: string,
  dealKind: string,
  sourceRef: string,
): SpotContractMarkPayload {
  return {
    mark_code: markCode.trim(),
    deal_kind: dealKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadSpotContractMarks(): Promise<SpotContractMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog spot/contract niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SpotContractMarkRow[]
}

export async function createSpotContractMark(
  payload: SpotContractMarkPayload,
): Promise<SpotContractMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "spot-contract-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika spot/contract odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SpotContractMarkRow
}
