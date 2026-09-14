import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type WmsFlowMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  flow_kind: string
  source_ref: string
}

export type WmsFlowMarkPayload = {
  mark_code: string
  flow_kind: string
  source_ref: string
}

const PATH = "/api/v1/wms-flow-marks"

export function buildWmsFlowMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): WmsFlowMarkPayload {
  return {
    mark_code: args.code.trim(),
    flow_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchWmsFlowMarks(): Promise<WmsFlowMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu WMS"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as WmsFlowMarkRow[]
}

export async function saveWmsFlowMark(payload: WmsFlowMarkPayload): Promise<WmsFlowMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "wms-flow-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać operacji WMS"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as WmsFlowMarkRow
}
