import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TermsAiMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  terms_kind: string
  source_ref: string
}

export type TermsAiMarkPayload = {
  mark_code: string
  terms_kind: string
  source_ref: string
}

const TERMS_AI_URL = "/api/v1/terms-ai-marks"

export function makeTermsAiMarkPayload(
  markCode: string,
  lezKind: string,
  sourceRef: string,
): TermsAiMarkPayload {
  return {
    mark_code: markCode.trim(),
    terms_kind: lezKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadTermsAiMarks(): Promise<TermsAiMarkRow[]> {
  const res = await fetch(TERMS_AI_URL, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Katalog Terms AI niedostepny"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as TermsAiMarkRow[]
}

export async function createTermsAiMark(payload: TermsAiMarkPayload): Promise<TermsAiMarkRow> {
  const res = await fetch(TERMS_AI_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "terms-ai-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis Terms AI odrzucony"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as TermsAiMarkRow
}
