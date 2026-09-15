import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type FieldConfidenceMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  band_kind: string
  source_ref: string
}

export type FieldConfidenceMarkPayload = {
  mark_code: string
  band_kind: string
  source_ref: string
}

const PATH = "/api/v1/field-confidence-marks"

export function buildFieldConfidenceMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): FieldConfidenceMarkPayload {
  return {
    mark_code: args.code.trim(),
    band_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchFieldConfidenceMarks(): Promise<FieldConfidenceMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu pewności per pole"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as FieldConfidenceMarkRow[]
}

export async function saveFieldConfidenceMark(
  payload: FieldConfidenceMarkPayload,
): Promise<FieldConfidenceMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "field-confidence-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać pasma pewności per pole"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as FieldConfidenceMarkRow
}
