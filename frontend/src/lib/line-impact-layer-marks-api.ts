import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LineImpactLayerMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  layer_kind: string
  source_ref: string
}

export type LineImpactLayerMarkPayload = {
  mark_code: string
  layer_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/line-impact-layer-marks"

export function buildLineImpactLayerMarkWrite(input: {
  code: string
  kind: string
  origin: string
}): LineImpactLayerMarkPayload {
  const mark_code = input.code.trim()
  const layer_kind = input.kind.trim().toLowerCase()
  const source_ref = input.origin.trim()
  return { mark_code, layer_kind, source_ref }
}

export async function fetchLineImpactLayerMarks(): Promise<LineImpactLayerMarkRow[]> {
  const response = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (response.ok) {
    return (await response.json()) as LineImpactLayerMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się wczytać warstw liczonych linii"),
    httpErrorStatus(response),
  )
}

export async function saveLineImpactLayerMark(
  body: LineImpactLayerMarkPayload,
): Promise<LineImpactLayerMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "line-impact-layer-hitl",
    },
    body: JSON.stringify(body),
  })
  if (response.status === 201) {
    return (await response.json()) as LineImpactLayerMarkRow
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się zapisać warstwy liczonej linii"),
    httpErrorStatus(response),
  )
}
