import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DemoWipeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  wipe_kind: string
  source_ref: string
}

export type DemoWipeMarkPayload = {
  mark_code: string
  wipe_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/demo-wipe-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeDemoWipeMarkPayload(
  markCode: string,
  wipeKind: string,
  sourceRef: string,
): DemoWipeMarkPayload {
  return {
    mark_code: markCode.trim(),
    wipe_kind: wipeKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadDemoWipeMarks(): Promise<DemoWipeMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog wipe demo niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DemoWipeMarkRow[]
}

export async function createDemoWipeMark(
  payload: DemoWipeMarkPayload,
): Promise<DemoWipeMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "demo-wipe-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika wipe demo odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DemoWipeMarkRow
}
