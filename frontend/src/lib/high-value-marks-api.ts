import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type HighValueMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  protocol_kind: string
  source_ref: string
}

export type HighValueMarkPayload = {
  mark_code: string
  protocol_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/high-value-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeHighValueMarkPayload(
  markCode: string,
  protocolKind: string,
  sourceRef: string,
): HighValueMarkPayload {
  return {
    mark_code: markCode.trim(),
    protocol_kind: protocolKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadHighValueMarks(): Promise<HighValueMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog protokolu high-value niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as HighValueMarkRow[]
}

export async function createHighValueMark(
  payload: HighValueMarkPayload,
): Promise<HighValueMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "high-value-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika protokolu high-value odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as HighValueMarkRow
}
