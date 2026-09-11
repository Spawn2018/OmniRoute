import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/schedule-exception-marks"

export type ScheduleExceptionMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  exception_kind: string
  source_ref: string
}

export type ScheduleExceptionMarkWrite = {
  mark_code: string
  exception_kind: string
  source_ref: string
}

export function buildScheduleExceptionMarkWrite(parts: {
  code: string
  kind: string
  origin: string
}): ScheduleExceptionMarkWrite {
  return {
    mark_code: parts.code.trim(),
    exception_kind: parts.kind.trim().toLowerCase(),
    source_ref: parts.origin.trim(),
  }
}

async function load<T>(response: Response, fail: string, ok: number): Promise<T> {
  if (response.status !== ok) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listScheduleExceptionMarks(): Promise<ScheduleExceptionMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  return load(response, "Lista schedule exception niedostępna", 200)
}

export async function saveScheduleExceptionMark(
  body: ScheduleExceptionMarkWrite,
): Promise<ScheduleExceptionMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return load(response, "Zapis schedule exception nieudany", 201)
}
