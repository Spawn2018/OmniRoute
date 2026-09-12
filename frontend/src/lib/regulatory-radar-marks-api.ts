import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RegulatoryRadarMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  radar_kind: string
  source_ref: string
}

export type RegulatoryRadarPayload = {
  mark_code: string
  radar_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/regulatory-radar-marks"

export function makeRegulatoryRadarPayload(
  code: string,
  kind: string,
  ref: string,
): RegulatoryRadarPayload {
  return {
    mark_code: code.trim(),
    radar_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadRegulatoryRadarMarks(): Promise<RegulatoryRadarMarkRow[]> {
  const packet = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (packet.ok) {
    return (await packet.json()) as RegulatoryRadarMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(packet, "Lista znacznikow regulatory radar niedostepna"),
    httpErrorStatus(packet),
  )
}

export async function createRegulatoryRadarMark(
  payload: RegulatoryRadarPayload,
): Promise<RegulatoryRadarMarkRow> {
  const packet = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (packet.status === 201) {
    return (await packet.json()) as RegulatoryRadarMarkRow
  }
  throw new ApiError(
    await readApiDetail(packet, "Zapis znacznika regulatory radar nieudany"),
    httpErrorStatus(packet),
  )
}
