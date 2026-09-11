import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/remediation-options"

export type RemediationOptionRow = {
  id: string
  organization_id: string
  option_code: string
  option_kind: string
  source_ref: string
}

export type RemediationOptionWrite = {
  option_code: string
  option_kind: string
  source_ref: string
}

export function buildRemediationWrite(fields: {
  code: string
  kind: string
  origin: string
}): RemediationOptionWrite {
  return {
    option_code: fields.code.trim(),
    option_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchRemediationOptions(): Promise<RemediationOptionRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy opcji naprawy", 200)
}

export async function saveRemediationOption(
  body: RemediationOptionWrite,
): Promise<RemediationOptionRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu opcji naprawy", 201)
}
