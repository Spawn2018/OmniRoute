import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type HandoverSbarMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  sbar_kind: string
  source_ref: string
}

export type HandoverSbarMarkPayload = {
  mark_code: string
  sbar_kind: string
  source_ref: string
}

const PATH = "/api/v1/handover-sbar-marks"

export function buildHandoverSbarMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): HandoverSbarMarkPayload {
  return {
    mark_code: args.code.trim(),
    sbar_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchHandoverSbarMarks(): Promise<HandoverSbarMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu SBAR"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as HandoverSbarMarkRow[]
}

export async function saveHandoverSbarMark(
  payload: HandoverSbarMarkPayload,
): Promise<HandoverSbarMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "handover-sbar-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika SBAR"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as HandoverSbarMarkRow
}
