import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DemoGpsMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  demo_kind: string
  source_ref: string
}

export type DemoGpsMarkPayload = {
  mark_code: string
  demo_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/demo-gps-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeDemoGpsMarkPayload(
  markCode: string,
  demoKind: string,
  sourceRef: string,
): DemoGpsMarkPayload {
  return {
    mark_code: markCode.trim(),
    demo_kind: demoKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadDemoGpsMarks(): Promise<DemoGpsMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog demo GPS niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DemoGpsMarkRow[]
}

export async function createDemoGpsMark(
  payload: DemoGpsMarkPayload,
): Promise<DemoGpsMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "demo-gps-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika demo GPS odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DemoGpsMarkRow
}
