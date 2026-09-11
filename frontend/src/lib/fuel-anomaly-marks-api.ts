import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const ENDPOINT = "/api/v1/fuel-anomaly-marks"

export type FuelAnomalyMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  anomaly_kind: string
  source_ref: string
}

type WriteBody = {
  mark_code: string
  anomaly_kind: string
  source_ref: string
}

export function makeFuelAnomalyBody(
  mark: string,
  kind: string,
  origin: string,
): WriteBody {
  return {
    mark_code: mark.trim(),
    anomaly_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function take<T>(res: Response, fail: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fail), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function fetchFuelAnomalyMarks(): Promise<FuelAnomalyMarkRow[]> {
  const res = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  return take(res, "Lista fuel anomaly niedostępna", 200)
}

export async function postFuelAnomalyMark(body: WriteBody): Promise<FuelAnomalyMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return take(res, "Zapis fuel anomaly nieudany", 201)
}
