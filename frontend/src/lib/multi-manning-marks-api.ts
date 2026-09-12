import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type MultiManningMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  manning_kind: string
  source_ref: string
}

export type MultiManningMarkPayload = {
  mark_code: string
  manning_kind: string
  source_ref: string
}

const CREW_MARKS_PATH = "/api/v1/multi-manning-marks"

export function makeMultiManningMarkPayload(
  markCode: string,
  manningKind: string,
  sourceRef: string,
): MultiManningMarkPayload {
  return {
    mark_code: markCode.trim(),
    manning_kind: manningKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadMultiManningMarks(): Promise<MultiManningMarkRow[]> {
  const response = await fetch(CREW_MARKS_PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Tryby multi-manning niedostepne"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MultiManningMarkRow[]
}

export async function createMultiManningMark(
  payload: MultiManningMarkPayload,
): Promise<MultiManningMarkRow> {
  const response = await fetch(CREW_MARKS_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "crew-manning-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis trybu zalogi odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as MultiManningMarkRow
}
