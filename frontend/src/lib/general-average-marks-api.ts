import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type GeneralAverageMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  average_kind: string
  source_ref: string
}

export type GeneralAveragePayload = {
  mark_code: string
  average_kind: string
  source_ref: string
}

const PATH = "/api/v1/general-average-marks"

export function makeGeneralAveragePayload(
  markCode: string,
  averageKind: string,
  sourceRef: string,
): GeneralAveragePayload {
  return {
    mark_code: markCode.trim(),
    average_kind: averageKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadGeneralAverageMarks(): Promise<GeneralAverageMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Lista znacznikow GA niedostepna"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as GeneralAverageMarkRow[]
}

export async function createGeneralAverageMark(
  payload: GeneralAveragePayload,
): Promise<GeneralAverageMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika GA nieudany"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as GeneralAverageMarkRow
}
