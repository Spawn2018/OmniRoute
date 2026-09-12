import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type AbandonedRtoMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  fate_kind: string
  source_ref: string
}

export type AbandonedRtoPayload = {
  mark_code: string
  fate_kind: string
  source_ref: string
}

const PATH = "/api/v1/abandoned-rto-marks"

export function makeAbandonedRtoPayload(
  markCode: string,
  fateKind: string,
  sourceRef: string,
): AbandonedRtoPayload {
  return {
    mark_code: markCode.trim(),
    fate_kind: fateKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

async function fail(response: Response, fallback: string): Promise<never> {
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function loadAbandonedRtoMarks(): Promise<AbandonedRtoMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  if (response.ok) {
    return (await response.json()) as AbandonedRtoMarkRow[]
  }
  return fail(response, "Lista losow abandoned/RTO niedostepna")
}

export async function createAbandonedRtoMark(
  payload: AbandonedRtoPayload,
): Promise<AbandonedRtoMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (response.status === 201) {
    return (await response.json()) as AbandonedRtoMarkRow
  }
  return fail(response, "Zapis losu abandoned/RTO nieudany")
}
