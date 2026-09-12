import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RoleViewMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  view_kind: string
  source_ref: string
}

export type RoleViewMarkPayload = {
  mark_code: string
  view_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/role-view-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeRoleViewMarkPayload(
  markCode: string,
  viewKind: string,
  sourceRef: string,
): RoleViewMarkPayload {
  return {
    mark_code: markCode.trim(),
    view_kind: viewKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadRoleViewMarks(): Promise<RoleViewMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog widoku roli niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as RoleViewMarkRow[]
}

export async function createRoleViewMark(
  payload: RoleViewMarkPayload,
): Promise<RoleViewMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "role-view-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis widoku roli odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as RoleViewMarkRow
}
