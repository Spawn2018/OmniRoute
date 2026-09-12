import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type MobileClientMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  client_kind: string
  source_ref: string
}

export type MobileClientMarkPayload = {
  mark_code: string
  client_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/mobile-client-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeMobileClientMarkPayload(
  markCode: string,
  clientKind: string,
  sourceRef: string,
): MobileClientMarkPayload {
  return {
    mark_code: markCode.trim(),
    client_kind: clientKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadMobileClientMarks(): Promise<MobileClientMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog klienta mobilnego niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MobileClientMarkRow[]
}

export async function createMobileClientMark(
  payload: MobileClientMarkPayload,
): Promise<MobileClientMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "mobile-client-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika klienta mobilnego odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MobileClientMarkRow
}
