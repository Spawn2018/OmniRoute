import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type EDoreczeniaMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  delivery_kind: string
  source_ref: string
}

export type EDoreczeniaMarkPayload = {
  mark_code: string
  delivery_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/e-doreczenia-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeEDoreczeniaMarkPayload(
  markCode: string,
  deliveryKind: string,
  sourceRef: string,
): EDoreczeniaMarkPayload {
  return {
    mark_code: markCode.trim(),
    delivery_kind: deliveryKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadEDoreczeniaMarks(): Promise<EDoreczeniaMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog e-Doręczenia niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as EDoreczeniaMarkRow[]
}

export async function createEDoreczeniaMark(
  payload: EDoreczeniaMarkPayload,
): Promise<EDoreczeniaMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "e-doreczenia-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika e-Doręczenia odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as EDoreczeniaMarkRow
}
