import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type LezMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  lez_kind: string
  source_ref: string
}

export type LezMarkPayload = {
  mark_code: string
  lez_kind: string
  source_ref: string
}

const LEZ_URL = "/api/v1/lez-marks"

export function makeLezMarkPayload(
  markCode: string,
  lezKind: string,
  sourceRef: string,
): LezMarkPayload {
  return {
    mark_code: markCode.trim(),
    lez_kind: lezKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadLezMarks(): Promise<LezMarkRow[]> {
  const res = await fetch(LEZ_URL, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Katalog LEZ niedostepny"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as LezMarkRow[]
}

export async function createLezMark(payload: LezMarkPayload): Promise<LezMarkRow> {
  const res = await fetch(LEZ_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "lez-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis LEZ odrzucony"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as LezMarkRow
}
