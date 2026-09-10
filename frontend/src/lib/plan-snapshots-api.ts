import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/plan-snapshots"

export type PlanSnapshotRow = {
  id: string
  organization_id: string
  snapshot_code: string
  shipment_id: string
  trip_id: string
  resource_id: string
  author_label: string
  recorded_at: string
  source_ref: string
}

export type PlanSnapshotWrite = {
  snapshot_code: string
  shipment_id: string
  trip_id: string
  resource_id: string
  author_label: string
  recorded_at: string
  source_ref: string
}

export function snapshotWrite(draft: {
  codeStamp: string
  shipmentStamp: string
  tripStamp: string
  resourceStamp: string
  authorStamp: string
  whenStamp: string
  originStamp: string
}): PlanSnapshotWrite {
  return {
    snapshot_code: draft.codeStamp.trim(),
    shipment_id: draft.shipmentStamp.trim(),
    trip_id: draft.tripStamp.trim(),
    resource_id: draft.resourceStamp.trim(),
    author_label: draft.authorStamp.trim(),
    recorded_at: draft.whenStamp.trim(),
    source_ref: draft.originStamp.trim(),
  }
}

async function parseSnapshot<T>(res: Response, fallback: string, ok: number): Promise<T> {
  if (res.status !== ok) {
    throw new ApiError(await readApiDetail(res, fallback), httpErrorStatus(res))
  }
  return (await res.json()) as T
}

export async function listPlanSnapshots(): Promise<PlanSnapshotRow[]> {
  return parseSnapshot(
    await fetch(PATH, { headers: requireAuthHeaders() }),
    "Błąd listy migawek planu",
    200,
  )
}

export async function persistSnapshot(payload: PlanSnapshotWrite): Promise<PlanSnapshotRow> {
  return parseSnapshot(
    await fetch(PATH, {
      method: "POST",
      headers: { ...requireAuthHeaders(), Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
    "Błąd zapisu migawki planu",
    201,
  )
}
