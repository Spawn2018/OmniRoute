import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/groupage-dispatcher-marks"

export type GroupageDispatcherMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  dispatcher_kind: string
  source_ref: string
}

export type GroupageDispatcherMarkWrite = {
  mark_code: string
  dispatcher_kind: string
  source_ref: string
}

export function buildGroupageDispatcherMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): GroupageDispatcherMarkWrite {
  return {
    mark_code: fields.code.trim(),
    dispatcher_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchGroupageDispatcherMarks(): Promise<GroupageDispatcherMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników dyspozytora drobnicy", 200)
}

export async function saveGroupageDispatcherMark(
  body: GroupageDispatcherMarkWrite,
): Promise<GroupageDispatcherMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika dyspozytora drobnicy", 201)
}
