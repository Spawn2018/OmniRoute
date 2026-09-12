import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CsrdMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  report_kind: string
  source_ref: string
}

export type CsrdMarkPayload = {
  mark_code: string
  report_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/csrd-marks"

export function makeCsrdMarkPayload(
  markCode: string,
  reportKind: string,
  sourceRef: string,
): CsrdMarkPayload {
  return {
    mark_code: markCode.trim(),
    report_kind: reportKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadCsrdMarks(): Promise<CsrdMarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu CSRD"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as CsrdMarkRow[]
}

export async function createCsrdMark(
  payload: CsrdMarkPayload,
): Promise<CsrdMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "csrd-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika CSRD"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as CsrdMarkRow
}
