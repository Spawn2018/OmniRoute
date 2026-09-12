import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type JobMetricMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  metric_kind: string
  source_ref: string
}

export type JobMetricMarkPayload = {
  mark_code: string
  metric_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/job-metric-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeJobMetricMarkPayload(
  markCode: string,
  metricKind: string,
  sourceRef: string,
): JobMetricMarkPayload {
  return {
    mark_code: markCode.trim(),
    metric_kind: metricKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadJobMetricMarks(): Promise<JobMetricMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog metryki jobu niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as JobMetricMarkRow[]
}

export async function createJobMetricMark(
  payload: JobMetricMarkPayload,
): Promise<JobMetricMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "job-metric-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika metryki jobu odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as JobMetricMarkRow
}
