import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type NamedPlaceMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  named_place: string
  terms_version: string
  source_ref: string
}

export type NamedPlaceMarkPayload = {
  mark_code: string
  named_place: string
  terms_version: string
  source_ref: string
}

const ENDPOINT = "/api/v1/named-place-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeNamedPlaceMarkPayload(
  markCode: string,
  namedPlace: string,
  termsVersion: string,
  sourceRef: string,
): NamedPlaceMarkPayload {
  return {
    mark_code: markCode.trim(),
    named_place: namedPlace.trim(),
    terms_version: termsVersion.trim(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadNamedPlaceMarks(): Promise<NamedPlaceMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog miejsca nazwanego niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as NamedPlaceMarkRow[]
}

export async function createNamedPlaceMark(
  payload: NamedPlaceMarkPayload,
): Promise<NamedPlaceMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "named-place-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika miejsca nazwanego odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as NamedPlaceMarkRow
}
