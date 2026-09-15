import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/extraction-prompt-marks" as const

export type ExtractionPromptMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  prompt_kind: string
  source_ref: string
}

export type ExtractionPromptMarkWrite = {
  mark_code: string
  prompt_kind: string
  source_ref: string
}

export function buildExtractionPromptMarkWrite(
  code: string,
  kind: string,
  origin: string,
): ExtractionPromptMarkWrite {
  return {
    mark_code: code.trim(),
    prompt_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function asJson<T>(response: Response, label: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, label), httpErrorStatus(response))
}

export async function fetchExtractionPromptMarks(): Promise<ExtractionPromptMarkRow[]> {
  return asJson(await fetch(PATH, { headers: requireAuthHeaders() }), "Błąd listy promptów", 200)
}

export async function saveExtractionPromptMark(
  body: ExtractionPromptMarkWrite,
): Promise<ExtractionPromptMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu promptu", 201)
}
