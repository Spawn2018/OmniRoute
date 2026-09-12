import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ReeferMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  reefer_kind: string
  source_ref: string
}

export type ReeferMarkPayload = {
  mark_code: string
  reefer_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/reefer-marks"

export function makeReeferMarkPayload(
  markCode: string,
  reeferKind: string,
  sourceRef: string,
): ReeferMarkPayload {
  return {
    mark_code: markCode.trim(),
    reefer_kind: reeferKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadReeferMarks(): Promise<ReeferMarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu reefer"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as ReeferMarkRow[]
}

export async function createReeferMark(
  payload: ReeferMarkPayload,
): Promise<ReeferMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "reefer-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika reefer"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as ReeferMarkRow
}
