import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/crm-pipeline-marks"

export type CrmPipelineMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  pipeline_kind: string
  source_ref: string
}

export type CrmPipelineMarkWrite = {
  mark_code: string
  pipeline_kind: string
  source_ref: string
}

export function buildCrmPipelineMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CrmPipelineMarkWrite {
  return {
    mark_code: fields.code.trim(),
    pipeline_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCrmPipelineMarks(): Promise<CrmPipelineMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy etapów CRM", 200)
}

export async function saveCrmPipelineMark(body: CrmPipelineMarkWrite): Promise<CrmPipelineMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu etapu CRM", 201)
}
