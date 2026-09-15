import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/shipper-award-marks" as const

export type ShipperAwardMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  award_kind: string
  source_ref: string
}

export type ShipperAwardMarkWrite = {
  mark_code: string
  award_kind: string
  source_ref: string
}

export function buildShipperAwardMarkWrite(
  code: string,
  kind: string,
  origin: string,
): ShipperAwardMarkWrite {
  return {
    mark_code: code.trim(),
    award_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function asJson<T>(response: Response, label: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, label), httpErrorStatus(response))
}

export async function fetchShipperAwardMarks(): Promise<ShipperAwardMarkRow[]> {
  return asJson(await fetch(PATH, { headers: requireAuthHeaders() }), "Błąd listy award", 200)
}

export async function saveShipperAwardMark(
  body: ShipperAwardMarkWrite,
): Promise<ShipperAwardMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu award", 201)
}
