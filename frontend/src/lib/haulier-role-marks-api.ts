import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type HaulierRoleMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  role_kind: string
  source_ref: string
}

export type HaulierRoleMarkPayload = {
  mark_code: string
  role_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/haulier-role-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeHaulierRoleMarkPayload(
  markCode: string,
  roleKind: string,
  sourceRef: string,
): HaulierRoleMarkPayload {
  return {
    mark_code: markCode.trim(),
    role_kind: roleKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadHaulierRoleMarks(): Promise<HaulierRoleMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog roli przewoznika niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as HaulierRoleMarkRow[]
}

export async function createHaulierRoleMark(
  payload: HaulierRoleMarkPayload,
): Promise<HaulierRoleMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "haulier-role-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika roli przewoznika odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as HaulierRoleMarkRow
}
