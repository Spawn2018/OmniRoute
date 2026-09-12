import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SlotGuaranteeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  stance_kind: string
  source_ref: string
}

export type SlotGuaranteeMarkPayload = {
  mark_code: string
  stance_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/slot-guarantee-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeSlotGuaranteeMarkPayload(
  markCode: string,
  stanceKind: string,
  sourceRef: string,
): SlotGuaranteeMarkPayload {
  return {
    mark_code: markCode.trim(),
    stance_kind: stanceKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadSlotGuaranteeMarks(): Promise<SlotGuaranteeMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog stance slotu niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SlotGuaranteeMarkRow[]
}

export async function createSlotGuaranteeMark(
  payload: SlotGuaranteeMarkPayload,
): Promise<SlotGuaranteeMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "slot-guarantee-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika stance slotu odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SlotGuaranteeMarkRow
}
