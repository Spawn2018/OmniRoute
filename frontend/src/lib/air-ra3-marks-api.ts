import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AirRa3MarkRow = {
  id: string
  organization_id: string
  mark_code: string
  air_kind: string
  source_ref: string
}

export type AirRa3MarkPayload = {
  mark_code: string
  air_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/air-ra3-marks"

export function makeAirRa3MarkPayload(
  markCode: string,
  airKind: string,
  sourceRef: string,
): AirRa3MarkPayload {
  return {
    mark_code: markCode.trim(),
    air_kind: airKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadAirRa3Marks(): Promise<AirRa3MarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu air RA3"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as AirRa3MarkRow[]
}

export async function createAirRa3Mark(
  payload: AirRa3MarkPayload,
): Promise<AirRa3MarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "air-ra3-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika air RA3"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as AirRa3MarkRow
}
