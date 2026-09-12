import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RailUicMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  rail_kind: string
  source_ref: string
}

export type RailUicMarkPayload = {
  mark_code: string
  rail_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/rail-uic-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeRailUicMarkPayload(
  markCode: string,
  railKind: string,
  sourceRef: string,
): RailUicMarkPayload {
  return {
    mark_code: markCode.trim(),
    rail_kind: railKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadRailUicMarks(): Promise<RailUicMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog UIC/CIM/SMGS niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as RailUicMarkRow[]
}

export async function createRailUicMark(
  payload: RailUicMarkPayload,
): Promise<RailUicMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "rail-uic-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika UIC/CIM/SMGS odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as RailUicMarkRow
}
