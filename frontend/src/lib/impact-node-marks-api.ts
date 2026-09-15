import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const IMPACT_NODE_MARKS_PATH = "/api/v1/impact-node-marks"

export type ImpactNodeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  node_kind: string
  source_ref: string
}

export type ImpactNodeMarkWrite = {
  mark_code: string
  node_kind: string
  source_ref: string
}

export function buildImpactNodeMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): ImpactNodeMarkWrite {
  const mark_code = fields.code.trim()
  const node_kind = fields.kind.trim().toLowerCase()
  const source_ref = fields.origin.trim()
  return { mark_code, node_kind, source_ref }
}

async function parseImpactNodeJson<T>(
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

export async function fetchImpactNodeMarks(): Promise<ImpactNodeMarkRow[]> {
  const response = await fetch(IMPACT_NODE_MARKS_PATH, { headers: requireAuthHeaders() })
  return parseImpactNodeJson(response, "Błąd listy znaczników impact node", 200)
}

export async function saveImpactNodeMark(
  body: ImpactNodeMarkWrite,
): Promise<ImpactNodeMarkRow> {
  const response = await fetch(IMPACT_NODE_MARKS_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return parseImpactNodeJson(response, "Błąd zapisu znacznika impact node", 201)
}
