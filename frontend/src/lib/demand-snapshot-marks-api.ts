import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type DemandSnapshotMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  snapshot_kind: string
  source_ref: string
}

export type DemandSnapshotMarkPayload = {
  mark_code: string
  snapshot_kind: string
  source_ref: string
}

const PATH = "/api/v1/demand-snapshot-marks"

export function makeDemandSnapshotMarkPayload(
  markCode: string,
  snapshotKind: string,
  sourceRef: string,
): DemandSnapshotMarkPayload {
  return {
    mark_code: markCode.trim(),
    snapshot_kind: snapshotKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadDemandSnapshotMarks(): Promise<DemandSnapshotMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  if (response.ok) {
    return (await response.json()) as DemandSnapshotMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(response, "Lista znacznikow demand snapshot niedostepna"),
    httpErrorStatus(response),
  )
}

export async function createDemandSnapshotMark(
  payload: DemandSnapshotMarkPayload,
): Promise<DemandSnapshotMarkRow> {
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
    return (await response.json()) as DemandSnapshotMarkRow
  }
  throw new ApiError(
    await readApiDetail(response, "Zapis znacznika demand snapshot nieudany"),
    httpErrorStatus(response),
  )
}
