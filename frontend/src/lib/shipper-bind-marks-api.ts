import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ShipperBindMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bind_kind: string
  source_ref: string
}

export type ShipperBindMarkWrite = {
  mark_code: string
  bind_kind: string
  source_ref: string
}

const SHIPPER_BIND_URL = "/api/v1/shipper-bind-marks"

export function buildShipperBindMarkWrite(
  markCode: string,
  bindKind: string,
  sourceRef: string,
): ShipperBindMarkWrite {
  const mark_code = markCode.trim()
  const bind_kind = bindKind.trim().toLowerCase()
  const source_ref = sourceRef.trim()
  return { mark_code, bind_kind, source_ref }
}

async function shipperBody<T>(
  response: Response,
  fail: string,
  expected: number,
): Promise<T> {
  if (response.status !== expected) {
    const detail = await readApiDetail(response, fail)
    throw new ApiError(detail, httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchShipperBindMarks(): Promise<ShipperBindMarkRow[]> {
  const response = await fetch(SHIPPER_BIND_URL, { headers: requireAuthHeaders() })
  return shipperBody(response, "Błąd listy bind załadowcy", 200)
}

export async function saveShipperBindMark(
  write: ShipperBindMarkWrite,
): Promise<ShipperBindMarkRow> {
  const response = await fetch(SHIPPER_BIND_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(write),
  })
  return shipperBody(response, "Błąd zapisu bind załadowcy", 201)
}
