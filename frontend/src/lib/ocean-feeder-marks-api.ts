import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OceanFeederMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  feeder_kind: string
  source_ref: string
}

export type OceanFeederMarkPayload = {
  mark_code: string
  feeder_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/ocean-feeder-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeOceanFeederMarkPayload(
  markCode: string,
  feederKind: string,
  sourceRef: string,
): OceanFeederMarkPayload {
  return {
    mark_code: markCode.trim(),
    feeder_kind: feederKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadOceanFeederMarks(): Promise<OceanFeederMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog feeder/short-sea niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OceanFeederMarkRow[]
}

export async function createOceanFeederMark(
  payload: OceanFeederMarkPayload,
): Promise<OceanFeederMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "ocean-feeder-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika feeder/short-sea odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OceanFeederMarkRow
}
