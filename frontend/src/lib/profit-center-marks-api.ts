import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ProfitCenterMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  center_kind: string
  source_ref: string
}

export type ProfitCenterMarkPayload = {
  mark_code: string
  center_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/profit-center-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeProfitCenterMarkPayload(
  markCode: string,
  centerKind: string,
  sourceRef: string,
): ProfitCenterMarkPayload {
  return {
    mark_code: markCode.trim(),
    center_kind: centerKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadProfitCenterMarks(): Promise<ProfitCenterMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog centrum zysku/kosztu niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ProfitCenterMarkRow[]
}

export async function createProfitCenterMark(
  payload: ProfitCenterMarkPayload,
): Promise<ProfitCenterMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "profit-center-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika centrum zysku/kosztu odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ProfitCenterMarkRow
}
