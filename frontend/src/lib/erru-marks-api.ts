import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ErruMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  check_kind: string
  source_ref: string
}

export type ErruMarkPayload = {
  mark_code: string
  check_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/erru-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeErruMarkPayload(
  markCode: string,
  checkKind: string,
  sourceRef: string,
): ErruMarkPayload {
  return {
    mark_code: markCode.trim(),
    check_kind: checkKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadErruMarks(): Promise<ErruMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog ERRU niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ErruMarkRow[]
}

export async function createErruMark(
  payload: ErruMarkPayload,
): Promise<ErruMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "erru-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika ERRU odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ErruMarkRow
}
