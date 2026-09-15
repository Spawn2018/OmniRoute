import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/shipper-like-marks"

export type ShipperLikeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  like_kind: string
  source_ref: string
}

export type ShipperLikeMarkWrite = {
  mark_code: string
  like_kind: string
  source_ref: string
}

export function buildShipperLikeMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): ShipperLikeMarkWrite {
  const mark_code = fields.code.trim()
  const like_kind = fields.kind.trim().toLowerCase()
  const source_ref = fields.origin.trim()
  return { mark_code, like_kind, source_ref }
}

async function parseBody<T>(response: Response, failLabel: string, want: number): Promise<T> {
  if (response.status !== want) {
    const detail = await readApiDetail(response, failLabel)
    throw new ApiError(detail, httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchShipperLikeMarks(): Promise<ShipperLikeMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  return parseBody(response, "Błąd listy stance like-for-like", 200)
}

export async function saveShipperLikeMark(
  body: ShipperLikeMarkWrite,
): Promise<ShipperLikeMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return parseBody(response, "Błąd zapisu stance like-for-like", 201)
}
