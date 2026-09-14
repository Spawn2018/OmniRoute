import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type StyleCascadeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  cascade_kind: string
  source_ref: string
}

export type StyleCascadeMarkPayload = {
  mark_code: string
  cascade_kind: string
  source_ref: string
}

const PATH = "/api/v1/style-cascade-marks"

export function buildStyleCascadeMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): StyleCascadeMarkPayload {
  return {
    mark_code: args.code.trim(),
    cascade_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchStyleCascadeMarks(): Promise<StyleCascadeMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu kaskady stylu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as StyleCascadeMarkRow[]
}

export async function saveStyleCascadeMark(
  payload: StyleCascadeMarkPayload,
): Promise<StyleCascadeMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "style-cascade-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać poziomu kaskady stylu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as StyleCascadeMarkRow
}
