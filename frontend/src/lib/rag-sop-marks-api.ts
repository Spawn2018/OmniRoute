import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RagSopMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  scope_kind: string
  source_ref: string
}

export type RagSopMarkPayload = {
  mark_code: string
  scope_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/rag-sop-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeRagSopMarkPayload(
  markCode: string,
  scopeKind: string,
  sourceRef: string,
): RagSopMarkPayload {
  return {
    mark_code: markCode.trim(),
    scope_kind: scopeKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadRagSopMarks(): Promise<RagSopMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog zakresu RAG niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as RagSopMarkRow[]
}

export async function createRagSopMark(
  payload: RagSopMarkPayload,
): Promise<RagSopMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "rag-sop-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis zakresu RAG odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as RagSopMarkRow
}
