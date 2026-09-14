import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AutomationBiasMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bias_kind: string
  source_ref: string
}

export type AutomationBiasMarkPayload = {
  mark_code: string
  bias_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/automation-bias-marks"

export function buildAutomationBiasMarkWrite(input: {
  code: string
  kind: string
  origin: string
}): AutomationBiasMarkPayload {
  const mark_code = input.code.trim()
  const bias_kind = input.kind.trim().toLowerCase()
  const source_ref = input.origin.trim()
  return { mark_code, bias_kind, source_ref }
}

export async function fetchAutomationBiasMarks(): Promise<AutomationBiasMarkRow[]> {
  const response = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (response.ok) {
    return (await response.json()) as AutomationBiasMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się wczytać wpisów mitygacji automation bias"),
    httpErrorStatus(response),
  )
}

export async function saveAutomationBiasMark(
  body: AutomationBiasMarkPayload,
): Promise<AutomationBiasMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "automation-bias-hitl",
    },
    body: JSON.stringify(body),
  })
  if (response.status === 201) {
    return (await response.json()) as AutomationBiasMarkRow
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się zapisać mitygacji automation bias"),
    httpErrorStatus(response),
  )
}
