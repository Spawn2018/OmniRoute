import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ChassisMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  chassis_kind: string
  source_ref: string
}

export type ChassisMarkPayload = {
  mark_code: string
  chassis_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/chassis-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeChassisMarkPayload(
  markCode: string,
  chassisKind: string,
  sourceRef: string,
): ChassisMarkPayload {
  return {
    mark_code: markCode.trim(),
    chassis_kind: chassisKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadChassisMarks(): Promise<ChassisMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog chassis/trailer niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ChassisMarkRow[]
}

export async function createChassisMark(
  payload: ChassisMarkPayload,
): Promise<ChassisMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "chassis-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika chassis odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ChassisMarkRow
}
