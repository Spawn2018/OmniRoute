import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const URL = "/api/v1/combined-transport-marks"

export type CombinedTransportMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  regime_kind: string
  source_ref: string
}

export type CombinedTransportWrite = {
  mark_code: string
  regime_kind: string
  source_ref: string
}

export function packCombinedTransportWrite(
  markCode: string,
  regime: string,
  source: string,
): CombinedTransportWrite {
  return {
    mark_code: markCode.trim(),
    regime_kind: regime.trim().toLowerCase(),
    source_ref: source.trim(),
  }
}

async function asJson<T>(response: Response, fail: string, want: number): Promise<T> {
  if (response.status !== want) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listCombinedTransportMarks(): Promise<CombinedTransportMarkRow[]> {
  const response = await fetch(URL, { headers: requireAuthHeaders() })
  return asJson(response, "Lista combined transport niedostępna", 200)
}

export async function saveCombinedTransportMark(
  body: CombinedTransportWrite,
): Promise<CombinedTransportMarkRow> {
  const response = await fetch(URL, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Zapis combined transport nieudany", 201)
}
