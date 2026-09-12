import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PoBatchMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  batch_kind: string
  source_ref: string
}

export type PoBatchMarkPayload = {
  mark_code: string
  batch_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/po-batch-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makePoBatchMarkPayload(
  markCode: string,
  batchKind: string,
  sourceRef: string,
): PoBatchMarkPayload {
  return {
    mark_code: markCode.trim(),
    batch_kind: batchKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadPoBatchMarks(): Promise<PoBatchMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog po batch niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PoBatchMarkRow[]
}

export async function createPoBatchMark(
  payload: PoBatchMarkPayload,
): Promise<PoBatchMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "po-batch-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika po batch odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as PoBatchMarkRow
}
