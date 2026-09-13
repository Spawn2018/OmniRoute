import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TachoPlanMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  constraint_kind: string
  source_ref: string
}

export type TachoPlanMarkPayload = {
  mark_code: string
  constraint_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/tacho-plan-marks"

export function makeTachoPlanMarkPayload(
  markCode: string,
  constraintKind: string,
  sourceRef: string,
): TachoPlanMarkPayload {
  return {
    mark_code: markCode.trim(),
    constraint_kind: constraintKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadTachoPlanMarks(): Promise<TachoPlanMarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu ograniczenia tacho"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as TachoPlanMarkRow[]
}

export async function createTachoPlanMark(
  payload: TachoPlanMarkPayload,
): Promise<TachoPlanMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "tacho-plan-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika ograniczenia tacho"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as TachoPlanMarkRow
}
