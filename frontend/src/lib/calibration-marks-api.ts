import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/calibration-marks"

export type CalibrationMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  sample_ready: string
  source_ref: string
}

export type CalibrationMarkWrite = {
  mark_code: string
  sample_ready: string
  source_ref: string
}

export function buildCalibrationWrite(fields: {
  code: string
  kind: string
  origin: string
}): CalibrationMarkWrite {
  return {
    mark_code: fields.code.trim(),
    sample_ready: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCalibrationMarks(): Promise<CalibrationMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników kalibracji", 200)
}

export async function saveCalibrationMark(
  body: CalibrationMarkWrite,
): Promise<CalibrationMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika kalibracji", 201)
}
