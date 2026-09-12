import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CopyBanMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  ban_kind: string
  source_ref: string
}

export type CopyBanMarkPayload = {
  mark_code: string
  ban_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/copy-ban-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeCopyBanMarkPayload(
  markCode: string,
  banKind: string,
  sourceRef: string,
): CopyBanMarkPayload {
  return {
    mark_code: markCode.trim(),
    ban_kind: banKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadCopyBanMarks(): Promise<CopyBanMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog zakazu copy niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CopyBanMarkRow[]
}

export async function createCopyBanMark(
  payload: CopyBanMarkPayload,
): Promise<CopyBanMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "copy-ban-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis zakazu copy odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CopyBanMarkRow
}
