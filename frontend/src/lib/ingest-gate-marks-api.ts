import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type IngestGateMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  gate_kind: string
  source_ref: string
}

export type IngestGateMarkPayload = {
  mark_code: string
  gate_kind: string
  source_ref: string
}

const PATH = "/api/v1/ingest-gate-marks"

export function buildIngestGateMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): IngestGateMarkPayload {
  return {
    mark_code: args.code.trim(),
    gate_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchIngestGateMarks(): Promise<IngestGateMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu brama ingest"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as IngestGateMarkRow[]
}

export async function saveIngestGateMark(
  payload: IngestGateMarkPayload,
): Promise<IngestGateMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "ingest-gate-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika brama ingest"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as IngestGateMarkRow
}
