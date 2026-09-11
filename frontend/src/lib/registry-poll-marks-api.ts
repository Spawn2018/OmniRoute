import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/registry-poll-marks"

export type RegistryPollMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  poll_kind: string
  source_ref: string
}

export type RegistryPollMarkWrite = {
  mark_code: string
  poll_kind: string
  source_ref: string
}

export function buildRegistryPollMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): RegistryPollMarkWrite {
  return {
    mark_code: fields.code.trim(),
    poll_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchRegistryPollMarks(): Promise<RegistryPollMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników yard", 200)
}

export async function saveRegistryPollMark(body: RegistryPollMarkWrite): Promise<RegistryPollMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika poll rejestru", 201)
}
