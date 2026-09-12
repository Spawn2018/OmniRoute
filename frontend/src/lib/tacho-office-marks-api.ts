import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TachoOfficeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  tacho_kind: string
  source_ref: string
}

export type TachoOfficeMarkPayload = {
  mark_code: string
  tacho_kind: string
  source_ref: string
}

const TACHO_URL = "/api/v1/tacho-office-marks"

export function makeTachoOfficeMarkPayload(
  markCode: string,
  tachoKind: string,
  sourceRef: string,
): TachoOfficeMarkPayload {
  return {
    mark_code: markCode.trim(),
    tacho_kind: tachoKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadTachoOfficeMarks(): Promise<TachoOfficeMarkRow[]> {
  const res = await fetch(TACHO_URL, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Tacho office niedostepne"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as TachoOfficeMarkRow[]
}

export async function createTachoOfficeMark(
  payload: TachoOfficeMarkPayload,
): Promise<TachoOfficeMarkRow> {
  const res = await fetch(TACHO_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "tacho-office-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis tacho office odrzucony"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as TachoOfficeMarkRow
}
