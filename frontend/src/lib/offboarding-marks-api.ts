import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OffboardingMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  offboard_kind: string
  source_ref: string
}

export type OffboardingPayload = {
  mark_code: string
  offboard_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/offboarding-marks"

export function makeOffboardingPayload(
  code: string,
  kind: string,
  ref: string,
): OffboardingPayload {
  return {
    mark_code: code.trim(),
    offboard_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadOffboardingMarks(): Promise<OffboardingMarkRow[]> {
  const pack = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (pack.ok) {
    return (await pack.json()) as OffboardingMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(pack, "Lista znacznikow offboarding niedostepna"),
    httpErrorStatus(pack),
  )
}

export async function createOffboardingMark(
  payload: OffboardingPayload,
): Promise<OffboardingMarkRow> {
  const pack = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (pack.status === 201) {
    return (await pack.json()) as OffboardingMarkRow
  }
  throw new ApiError(
    await readApiDetail(pack, "Zapis znacznika offboarding nieudany"),
    httpErrorStatus(pack),
  )
}
