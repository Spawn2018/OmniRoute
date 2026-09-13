import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LoadOrderMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  order_kind: string
  source_ref: string
}

export type LoadOrderMarkPayload = {
  mark_code: string
  order_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/load-order-marks"

export function makeLoadOrderMarkPayload(
  markCode: string,
  orderKind: string,
  sourceRef: string,
): LoadOrderMarkPayload {
  return {
    mark_code: markCode.trim(),
    order_kind: orderKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadLoadOrderMarks(): Promise<LoadOrderMarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu kolejności załadunku"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as LoadOrderMarkRow[]
}

export async function createLoadOrderMark(
  payload: LoadOrderMarkPayload,
): Promise<LoadOrderMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "load-order-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika kolejności załadunku"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as LoadOrderMarkRow
}
