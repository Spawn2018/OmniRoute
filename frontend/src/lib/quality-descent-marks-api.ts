import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type QualityDescentMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  descent_kind: string
  source_ref: string
}

export type QualityDescentMarkPayload = {
  mark_code: string
  descent_kind: string
  source_ref: string
}

const PATH = "/api/v1/quality-descent-marks"

export function buildQualityDescentMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): QualityDescentMarkPayload {
  return {
    mark_code: args.code.trim(),
    descent_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchQualityDescentMarks(): Promise<QualityDescentMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu zejścia jakości"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as QualityDescentMarkRow[]
}

export async function saveQualityDescentMark(
  payload: QualityDescentMarkPayload,
): Promise<QualityDescentMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "quality-descent-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać powodu zejścia jakości"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as QualityDescentMarkRow
}
