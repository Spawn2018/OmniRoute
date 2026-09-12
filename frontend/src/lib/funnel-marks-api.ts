import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FunnelMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  funnel_kind: string
  source_ref: string
}

export type FunnelMarkPayload = {
  mark_code: string
  funnel_kind: string
  source_ref: string
}

const FUNNEL_URL = "/api/v1/funnel-marks"

export function makeFunnelMarkPayload(
  markCode: string,
  lezKind: string,
  sourceRef: string,
): FunnelMarkPayload {
  return {
    mark_code: markCode.trim(),
    funnel_kind: lezKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadFunnelMarks(): Promise<FunnelMarkRow[]> {
  const res = await fetch(FUNNEL_URL, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Katalog X7 lejek niedostepny"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as FunnelMarkRow[]
}

export async function createFunnelMark(payload: FunnelMarkPayload): Promise<FunnelMarkRow> {
  const res = await fetch(FUNNEL_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "funnel-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis X7 lejek odrzucony"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as FunnelMarkRow
}
