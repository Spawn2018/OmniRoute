import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OpsRoomMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  layer_kind: string
  source_ref: string
}

export type OpsRoomMarkPayload = {
  mark_code: string
  layer_kind: string
  source_ref: string
}

const PATH = "/api/v1/ops-room-marks"

export function buildOpsRoomMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): OpsRoomMarkPayload {
  return {
    mark_code: args.code.trim(),
    layer_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchOpsRoomMarks(): Promise<OpsRoomMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu sali operacyjnej"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as OpsRoomMarkRow[]
}

export async function saveOpsRoomMark(
  payload: OpsRoomMarkPayload,
): Promise<OpsRoomMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "ops-room-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać warstwy sali operacyjnej"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as OpsRoomMarkRow
}
