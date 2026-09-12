import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type EmptyDepotMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  depot_kind: string
  source_ref: string
}

export type EmptyDepotMarkPayload = {
  mark_code: string
  depot_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/empty-depot-marks"

export function makeEmptyDepotMarkPayload(
  markCode: string,
  depotKind: string,
  sourceRef: string,
): EmptyDepotMarkPayload {
  return {
    mark_code: markCode.trim(),
    depot_kind: depotKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadEmptyDepotMarks(): Promise<EmptyDepotMarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu empty/depot"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as EmptyDepotMarkRow[]
}

export async function createEmptyDepotMark(
  payload: EmptyDepotMarkPayload,
): Promise<EmptyDepotMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "empty-depot-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika empty/depot"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as EmptyDepotMarkRow
}
