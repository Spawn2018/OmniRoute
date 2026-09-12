import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AbSusMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  trial_kind: string
  source_ref: string
}

export type AbSusMarkPayload = {
  mark_code: string
  trial_kind: string
  source_ref: string
}

const AB_SUS_URL = "/api/v1/ab-sus-marks"

export function makeAbSusMarkPayload(
  markCode: string,
  lezKind: string,
  sourceRef: string,
): AbSusMarkPayload {
  return {
    mark_code: markCode.trim(),
    trial_kind: lezKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadAbSusMarks(): Promise<AbSusMarkRow[]> {
  const res = await fetch(AB_SUS_URL, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Katalog A/B+SUS niedostepny"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as AbSusMarkRow[]
}

export async function createAbSusMark(payload: AbSusMarkPayload): Promise<AbSusMarkRow> {
  const res = await fetch(AB_SUS_URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "ab-sus-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Zapis A/B+SUS odrzucony"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as AbSusMarkRow
}
