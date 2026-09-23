import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LocalChargeBindMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  bind_kind: string
  source_ref: string
}

export type LocalChargeBindMarkWrite = {
  mark_code: string
  bind_kind: string
  source_ref: string
}

const LIST_PATH = "/api/v1/local-charge-bind-marks"

export function buildLocalChargeBindMarkWrite(
  code: string,
  kind: string,
  origin: string,
): LocalChargeBindMarkWrite {
  return {
    mark_code: code.trim(),
    bind_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

export async function fetchLocalChargeBindMarks(): Promise<LocalChargeBindMarkRow[]> {
  const response = await fetch(LIST_PATH, { headers: requireAuthHeaders() })
  if (response.status !== 200) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy wiązań dopłaty lokalnej"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as LocalChargeBindMarkRow[]
}

export async function saveLocalChargeBindMark(
  payload: LocalChargeBindMarkWrite,
): Promise<LocalChargeBindMarkRow> {
  const response = await fetch(LIST_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu wiązania dopłaty lokalnej"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as LocalChargeBindMarkRow
}
