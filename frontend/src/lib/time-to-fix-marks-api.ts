import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const TIME_TO_FIX_PATH = "/api/v1/time-to-fix-marks"

export type TimeToFixMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  fix_kind: string
  source_ref: string
}

export type TimeToFixMarkWrite = {
  mark_code: string
  fix_kind: string
  source_ref: string
}

export function buildTimeToFixMarkWrite(input: {
  code: string
  kind: string
  origin: string
}): TimeToFixMarkWrite {
  const mark_code = input.code.trim()
  const fix_kind = input.kind.trim().toLowerCase()
  const source_ref = input.origin.trim()
  return { mark_code, fix_kind, source_ref }
}

async function expectJson<T>(
  response: Response,
  failLabel: string,
  expected: number,
): Promise<T> {
  if (response.status === expected) {
    return (await response.json()) as T
  }
  const detail = await readApiDetail(response, failLabel)
  throw new ApiError(detail, httpErrorStatus(response))
}

export async function listTimeToFixMarks(): Promise<TimeToFixMarkRow[]> {
  const response = await fetch(TIME_TO_FIX_PATH, { headers: requireAuthHeaders() })
  return expectJson(response, "Lista TIME-TO-FIX niedostępna", 200)
}

export async function saveTimeToFixMark(body: TimeToFixMarkWrite): Promise<TimeToFixMarkRow> {
  const response = await fetch(TIME_TO_FIX_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return expectJson(response, "Zapis TIME-TO-FIX nieudany", 201)
}
