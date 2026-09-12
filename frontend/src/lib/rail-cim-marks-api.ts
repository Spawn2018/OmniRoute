import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RailCimMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  rail_kind: string
  source_ref: string
}

export type RailCimMarkPayload = {
  mark_code: string
  rail_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/rail-cim-marks"

export function makeRailCimMarkPayload(
  markCode: string,
  railKind: string,
  sourceRef: string,
): RailCimMarkPayload {
  return {
    mark_code: markCode.trim(),
    rail_kind: railKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadRailCimMarks(): Promise<RailCimMarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu rail CIM"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as RailCimMarkRow[]
}

export async function createRailCimMark(
  payload: RailCimMarkPayload,
): Promise<RailCimMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "rail-cim-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika rail CIM"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as RailCimMarkRow
}
