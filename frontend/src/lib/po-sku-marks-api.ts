import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PoSkuMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  sku_kind: string
  source_ref: string
}

export type PoSkuMarkPayload = {
  mark_code: string
  sku_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/po-sku-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makePoSkuMarkPayload(
  markCode: string,
  skuKind: string,
  sourceRef: string,
): PoSkuMarkPayload {
  return {
    mark_code: markCode.trim(),
    sku_kind: skuKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadPoSkuMarks(): Promise<PoSkuMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog po sku niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PoSkuMarkRow[]
}

export async function createPoSkuMark(
  payload: PoSkuMarkPayload,
): Promise<PoSkuMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "po-sku-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika po sku odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PoSkuMarkRow
}
