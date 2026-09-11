import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/fleet-cost-marks"

export type FleetCostMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  cost_kind: string
  source_ref: string
}

export type FleetCostWrite = {
  mark_code: string
  cost_kind: string
  source_ref: string
}

export function packFleetCostWrite(
  code: string,
  kind: string,
  origin: string,
): FleetCostWrite {
  return {
    mark_code: code.trim(),
    cost_kind: kind.trim().toLowerCase(),
    source_ref: origin.trim(),
  }
}

async function loadJson<T>(res: Response, fail: string, ok: number): Promise<T> {
  if (res.status === ok) {
    return (await res.json()) as T
  }
  throw new ApiError(await readApiDetail(res, fail), httpErrorStatus(res))
}

export async function listFleetCostMarks(): Promise<FleetCostMarkRow[]> {
  const res = await fetch(PATH, { headers: requireAuthHeaders() })
  return loadJson(res, "Lista fleet cost niedostępna", 200)
}

export async function saveFleetCostMark(body: FleetCostWrite): Promise<FleetCostMarkRow> {
  const res = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return loadJson(res, "Zapis fleet cost nieudany", 201)
}
