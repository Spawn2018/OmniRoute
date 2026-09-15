import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const IMPACT_EDGE_MARKS_PATH = "/api/v1/impact-edge-marks"

export type ImpactEdgeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  from_kind: string
  to_kind: string
  source_ref: string
}

export type ImpactEdgeMarkWrite = {
  mark_code: string
  from_kind: string
  to_kind: string
  source_ref: string
}

export function buildImpactEdgeMarkWrite(fields: {
  code: string
  fromKind: string
  toKind: string
  origin: string
}): ImpactEdgeMarkWrite {
  const mark_code = fields.code.trim()
  const from_kind = fields.fromKind.trim().toLowerCase()
  const to_kind = fields.toKind.trim().toLowerCase()
  const source_ref = fields.origin.trim()
  return { mark_code, from_kind, to_kind, source_ref }
}

async function parseImpactEdgeJson<T>(
  response: Response,
  failMessage: string,
  expectedStatus: number,
): Promise<T> {
  if (response.status !== expectedStatus) {
    const detail = await readApiDetail(response, failMessage)
    throw new ApiError(detail, httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchImpactEdgeMarks(): Promise<ImpactEdgeMarkRow[]> {
  const response = await fetch(IMPACT_EDGE_MARKS_PATH, { headers: requireAuthHeaders() })
  return parseImpactEdgeJson(response, "Błąd listy znaczników impact edge", 200)
}

export async function saveImpactEdgeMark(
  body: ImpactEdgeMarkWrite,
): Promise<ImpactEdgeMarkRow> {
  const response = await fetch(IMPACT_EDGE_MARKS_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return parseImpactEdgeJson(response, "Błąd zapisu znacznika impact edge", 201)
}
