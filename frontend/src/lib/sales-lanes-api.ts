import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/sales-lanes"

export type SalesLaneRow = {
  id: string
  organization_id: string
  lane_code: string
  lane_kind: string
  origin_unlocode: string
  destination_unlocode: string
  source_ref: string
}

export type SalesLaneWrite = {
  lane_code: string
  lane_kind: string
  origin_unlocode: string
  destination_unlocode: string
  source_ref: string
}

export function buildSalesLaneWrite(fields: {
  code: string
  kind: string
  originCode: string
  destCode: string
  origin: string
}): SalesLaneWrite {
  return {
    lane_code: fields.code.trim(),
    lane_kind: fields.kind.trim().toLowerCase(),
    origin_unlocode: fields.originCode.trim().toUpperCase(),
    destination_unlocode: fields.destCode.trim().toUpperCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchSalesLanes(): Promise<SalesLaneRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy korytarzy sprzedażowych", 200)
}

export async function saveSalesLane(body: SalesLaneWrite): Promise<SalesLaneRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu korytarza sprzedażowego", 201)
}
