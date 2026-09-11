import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const URL = "/api/v1/subcontract-edge-marks"

export type SubcontractEdgeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  edge_kind: string
  source_ref: string
}

export type SubcontractEdgeMarkWrite = {
  mark_code: string
  edge_kind: string
  source_ref: string
}

export function buildSubcontractEdgeMarkWrite(parts: {
  code: string
  kind: string
  origin: string
}): SubcontractEdgeMarkWrite {
  return {
    mark_code: parts.code.trim(),
    edge_kind: parts.kind.trim().toLowerCase(),
    source_ref: parts.origin.trim(),
  }
}

async function unpack<T>(response: Response, fail: string, ok: number): Promise<T> {
  if (response.status !== ok) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listSubcontractEdgeMarks(): Promise<SubcontractEdgeMarkRow[]> {
  const response = await fetch(URL, { headers: requireAuthHeaders() })
  return unpack(response, "Lista subcontract edge niedostępna", 200)
}

export async function saveSubcontractEdgeMark(
  body: SubcontractEdgeMarkWrite,
): Promise<SubcontractEdgeMarkRow> {
  const response = await fetch(URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return unpack(response, "Zapis subcontract edge nieudany", 201)
}
