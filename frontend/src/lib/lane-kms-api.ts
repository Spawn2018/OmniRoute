import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/lane-kms"

export type LaneKmRow = {
  id: string
  organization_id: string
  km_code: string
  loaded_km: string
  empty_km: string
  approach_km: string
  source_ref: string
}

export type LaneKmWrite = {
  km_code: string
  loaded_km: string
  empty_km: string
  approach_km: string
  source_ref: string
}

export function laneKmWrite(draft: {
  codeStamp: string
  loadedStamp: string
  emptyStamp: string
  approachStamp: string
  originStamp: string
}): LaneKmWrite {
  return {
    km_code: draft.codeStamp.trim(),
    loaded_km: draft.loadedStamp.trim(),
    empty_km: draft.emptyStamp.trim(),
    approach_km: draft.approachStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseLaneKm<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listLaneKms(): Promise<LaneKmRow[]> {
  return parseLaneKm(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy km korytarza",
    200,
  )
}

export async function persistLaneKm(payload: LaneKmWrite): Promise<LaneKmRow> {
  return parseLaneKm(
    await fetch(PATH, {
      method: "POST",
      headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
    "Błąd zapisu km korytarza",
    201,
  )
}
