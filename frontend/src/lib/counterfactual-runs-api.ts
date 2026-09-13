import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CounterfactualRunRow = {
  id: string
  organization_id: string
  run_code: string
  baseline_label: string
  levers_label: string
  result_label: string
  source_ref: string
}

export type CounterfactualRunPayload = {
  run_code: string
  baseline_label: string
  levers_label: string
  result_label: string
  source_ref: string
}

const ENDPOINT = "/api/v1/counterfactual-runs" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeCounterfactualRunPayload(draft: {
  runCode: string
  baselineLabel: string
  leversLabel: string
  resultLabel: string
  sourceRef: string
}): CounterfactualRunPayload {
  return {
    run_code: draft.runCode.trim(),
    baseline_label: draft.baselineLabel.trim(),
    levers_label: draft.leversLabel.trim(),
    result_label: draft.resultLabel.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadCounterfactualRuns(): Promise<CounterfactualRunRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog przebiegu what-if niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CounterfactualRunRow[]
}

export async function createCounterfactualRun(
  payload: CounterfactualRunPayload,
): Promise<CounterfactualRunRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "counterfactual-run-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis przebiegu what-if odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CounterfactualRunRow
}
