import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RiskRegisterMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  risk_kind: string
  source_ref: string
}

export type RiskRegisterMarkPayload = {
  mark_code: string
  risk_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/risk-register-marks"

export function buildRiskRegisterMarkWrite(input: {
  code: string
  kind: string
  origin: string
}): RiskRegisterMarkPayload {
  const mark_code = input.code.trim()
  const risk_kind = input.kind.trim().toLowerCase()
  const source_ref = input.origin.trim()
  return { mark_code, risk_kind, source_ref }
}

export async function fetchRiskRegisterMarks(): Promise<RiskRegisterMarkRow[]> {
  const response = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (response.ok) {
    return (await response.json()) as RiskRegisterMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się wczytać wpisów rejestru ryzyka"),
    httpErrorStatus(response),
  )
}

export async function saveRiskRegisterMark(
  body: RiskRegisterMarkPayload,
): Promise<RiskRegisterMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "risk-register-hitl",
    },
    body: JSON.stringify(body),
  })
  if (response.status === 201) {
    return (await response.json()) as RiskRegisterMarkRow
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się zapisać rejestru ryzyka"),
    httpErrorStatus(response),
  )
}
