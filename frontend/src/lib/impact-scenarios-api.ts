import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/impact-scenarios"

export type ImpactScenarioRow = {
  id: string
  organization_id: string
  scenario_code: string
  chain_label: string
  source_ref: string
}

export type ImpactScenarioWrite = {
  scenario_code: string
  chain_label: string
  source_ref: string
}

export function buildImpactWrite(fields: {
  code: string
  label: string
  origin: string
}): ImpactScenarioWrite {
  return {
    scenario_code: fields.code.trim(),
    chain_label: fields.label.trim(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchImpactScenarios(): Promise<ImpactScenarioRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy scenariuszy skutku", 200)
}

export async function saveImpactScenario(body: ImpactScenarioWrite): Promise<ImpactScenarioRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu scenariusza skutku", 201)
}
