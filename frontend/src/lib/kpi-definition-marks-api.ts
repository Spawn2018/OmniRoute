import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type KpiDefinitionMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  kpi_kind: string
  source_ref: string
}

export type KpiDefinitionMarkPayload = {
  mark_code: string
  kpi_kind: string
  source_ref: string
}

const PATH = "/api/v1/kpi-definition-marks"

export function buildKpiDefinitionMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): KpiDefinitionMarkPayload {
  return {
    mark_code: args.code.trim(),
    kpi_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchKpiDefinitionMarks(): Promise<KpiDefinitionMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu definicji KPI"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as KpiDefinitionMarkRow[]
}

export async function saveKpiDefinitionMark(
  payload: KpiDefinitionMarkPayload,
): Promise<KpiDefinitionMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "kpi-definition-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika definicji KPI"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as KpiDefinitionMarkRow
}
