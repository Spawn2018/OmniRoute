import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LanguageCodeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  locale_kind: string
  source_ref: string
}

export type LanguageCodeMarkPayload = {
  mark_code: string
  locale_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/language-code-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeLanguageCodeMarkPayload(
  markCode: string,
  localeKind: string,
  sourceRef: string,
): LanguageCodeMarkPayload {
  return {
    mark_code: markCode.trim(),
    locale_kind: localeKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadLanguageCodeMarks(): Promise<LanguageCodeMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog kodu jezyka niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as LanguageCodeMarkRow[]
}

export async function createLanguageCodeMark(
  payload: LanguageCodeMarkPayload,
): Promise<LanguageCodeMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "language-code-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika kodu jezyka odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as LanguageCodeMarkRow
}
