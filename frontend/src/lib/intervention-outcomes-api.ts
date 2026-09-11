import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/intervention-outcomes"

export type InterventionOutcomeRow = {
  id: string
  organization_id: string
  outcome_code: string
  result_kind: string
  source_ref: string
}

export type InterventionOutcomeWrite = {
  outcome_code: string
  result_kind: string
  source_ref: string
}

export function buildInterventionOutcomeWrite(fields: {
  code: string
  kind: string
  origin: string
}): InterventionOutcomeWrite {
  return {
    outcome_code: fields.code.trim(),
    result_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchInterventionOutcomes(): Promise<InterventionOutcomeRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy wyników interwencji", 200)
}

export async function saveInterventionOutcome(
  body: InterventionOutcomeWrite,
): Promise<InterventionOutcomeRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu wyniku interwencji", 201)
}
