import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OceanAllianceMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  ocean_kind: string
  source_ref: string
}

export type OceanAllianceMarkPayload = {
  mark_code: string
  ocean_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/ocean-alliance-marks"

export function makeOceanAllianceMarkPayload(
  markCode: string,
  oceanKind: string,
  sourceRef: string,
): OceanAllianceMarkPayload {
  return {
    mark_code: markCode.trim(),
    ocean_kind: oceanKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadOceanAllianceMarks(): Promise<OceanAllianceMarkRow[]> {
  const res = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!res.ok) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się wczytać katalogu ocean alliance"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as OceanAllianceMarkRow[]
}

export async function createOceanAllianceMark(
  payload: OceanAllianceMarkPayload,
): Promise<OceanAllianceMarkRow> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "ocean-alliance-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (res.status !== 201) {
    throw new ApiError(
      await readApiDetail(res, "Nie udało się zapisać znacznika ocean alliance"),
      httpErrorStatus(res),
    )
  }
  return (await res.json()) as OceanAllianceMarkRow
}
