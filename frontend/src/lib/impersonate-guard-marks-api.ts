import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ImpersonateGuardMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  guard_kind: string
  source_ref: string
}

export type ImpersonateGuardMarkPayload = {
  mark_code: string
  guard_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/impersonate-guard-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeImpersonateGuardMarkPayload(
  markCode: string,
  guardKind: string,
  sourceRef: string,
): ImpersonateGuardMarkPayload {
  return {
    mark_code: markCode.trim(),
    guard_kind: guardKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadImpersonateGuardMarks(): Promise<ImpersonateGuardMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog impersonate guard niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ImpersonateGuardMarkRow[]
}

export async function createImpersonateGuardMark(
  payload: ImpersonateGuardMarkPayload,
): Promise<ImpersonateGuardMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "impersonate-guard-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika impersonate guard odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ImpersonateGuardMarkRow
}
