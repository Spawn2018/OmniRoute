import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/shipper-tender-marks"

export type ShipperTenderMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  shipper_kind: string
  source_ref: string
}

export type ShipperTenderMarkWrite = {
  mark_code: string
  shipper_kind: string
  source_ref: string
}

export function buildShipperTenderMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): ShipperTenderMarkWrite {
  return {
    mark_code: fields.code.trim(),
    shipper_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchShipperTenderMarks(): Promise<ShipperTenderMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy trybów przetargu załadowcy", 200)
}

export async function saveShipperTenderMark(
  body: ShipperTenderMarkWrite,
): Promise<ShipperTenderMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu trybu przetargu załadowcy", 201)
}
