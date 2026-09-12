import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DemoSimMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  sim_kind: string
  source_ref: string
}

export type DemoSimMarkPayload = {
  mark_code: string
  sim_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/demo-sim-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeDemoSimMarkPayload(
  markCode: string,
  simKind: string,
  sourceRef: string,
): DemoSimMarkPayload {
  return {
    mark_code: markCode.trim(),
    sim_kind: simKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadDemoSimMarks(): Promise<DemoSimMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog demo sim niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DemoSimMarkRow[]
}

export async function createDemoSimMark(
  payload: DemoSimMarkPayload,
): Promise<DemoSimMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "demo-sim-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika demo sim odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as DemoSimMarkRow
}
