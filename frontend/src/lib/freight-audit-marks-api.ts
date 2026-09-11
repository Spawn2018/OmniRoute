import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/freight-audit-marks"

export type FreightAuditMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  audit_kind: string
  source_ref: string
}

export type FreightAuditWrite = {
  mark_code: string
  audit_kind: string
  source_ref: string
}

export function buildFreightAuditWrite(input: {
  code: string
  kind: string
  origin: string
}): FreightAuditWrite {
  return {
    mark_code: input.code.trim(),
    audit_kind: input.kind.trim().toLowerCase(),
    source_ref: input.origin.trim(),
  }
}

async function asJson<T>(response: Response, fail: string, ok: number): Promise<T> {
  if (response.status !== ok) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchFreightAuditMarks(): Promise<FreightAuditMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników audytu frachtu", 200)
}

export async function saveFreightAuditMark(
  body: FreightAuditWrite,
): Promise<FreightAuditMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika audytu frachtu", 201)
}
