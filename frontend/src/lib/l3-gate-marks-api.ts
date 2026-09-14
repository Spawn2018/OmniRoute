import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type L3GateMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  gate_kind: string
  source_ref: string
}

export type L3GateMarkPayload = {
  mark_code: string
  gate_kind: string
  source_ref: string
}

const PATH = "/api/v1/l3-gate-marks"

export function buildL3GateMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): L3GateMarkPayload {
  return {
    mark_code: args.code.trim(),
    gate_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchL3GateMarks(): Promise<L3GateMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu bramy L3"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as L3GateMarkRow[]
}

export async function saveL3GateMark(
  payload: L3GateMarkPayload,
): Promise<L3GateMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "l3-gate-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika bramy L3"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as L3GateMarkRow
}
