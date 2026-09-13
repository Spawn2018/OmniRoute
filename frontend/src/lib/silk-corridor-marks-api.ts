import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SilkCorridorMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  corridor_kind: string
  source_ref: string
}

export type SilkCorridorMarkPayload = {
  mark_code: string
  corridor_kind: string
  source_ref: string
}

const PATH = "/api/v1/silk-corridor-marks"

export function buildSilkCorridorMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): SilkCorridorMarkPayload {
  return {
    mark_code: args.code.trim(),
    corridor_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchSilkCorridorMarks(): Promise<SilkCorridorMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu Jedwabnego Szlaku"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as SilkCorridorMarkRow[]
}

export async function saveSilkCorridorMark(
  payload: SilkCorridorMarkPayload,
): Promise<SilkCorridorMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "silk-corridor-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać stance korytarza Jedwabnego Szlaku"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as SilkCorridorMarkRow
}
