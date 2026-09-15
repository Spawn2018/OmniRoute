import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/shipper-round-marks"

export type ShipperRoundMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  round_kind: string
  source_ref: string
}

export type ShipperRoundMarkWrite = {
  mark_code: string
  round_kind: string
  source_ref: string
}

export function buildShipperRoundMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): ShipperRoundMarkWrite {
  return {
    mark_code: fields.code.trim(),
    round_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchShipperRoundMarks(): Promise<ShipperRoundMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy rund przetargu załadowcy", 200)
}

export async function saveShipperRoundMark(
  body: ShipperRoundMarkWrite,
): Promise<ShipperRoundMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu rundy przetargu załadowcy", 201)
}
