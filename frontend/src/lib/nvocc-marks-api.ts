import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type NvoccMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  nvocc_kind: string
  source_ref: string
}

export type NvoccMarkPayload = {
  mark_code: string
  nvocc_kind: string
  source_ref: string
}

const NVOCC_MARKS_URL = "/api/v1/nvocc-marks"

function authJsonHeaders(): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
  }
}

export function makeNvoccMarkPayload(
  markCode: string,
  nvoccKind: string,
  sourceRef: string,
): NvoccMarkPayload {
  return {
    mark_code: markCode.trim(),
    nvocc_kind: nvoccKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadNvoccMarks(): Promise<NvoccMarkRow[]> {
  const response = await fetch(NVOCC_MARKS_URL, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog NVOCC niedostępny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as NvoccMarkRow[]
}

export async function createNvoccMark(
  body: NvoccMarkPayload,
): Promise<NvoccMarkRow> {
  const response = await fetch(NVOCC_MARKS_URL, {
    method: "POST",
    headers: {
      ...authJsonHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Intent": "nvocc-role-hitl",
    },
    body: JSON.stringify(body),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis roli NVOCC odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as NvoccMarkRow
}
