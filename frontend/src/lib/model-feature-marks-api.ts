import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ModelFeatureMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  feature_kind: string
  source_ref: string
}

export type ModelFeatureMarkPayload = {
  mark_code: string
  feature_kind: string
  source_ref: string
}

const PATH = "/api/v1/model-feature-marks"

export function buildModelFeatureMarkWrite(args: {
  code: string
  kind: string
  origin: string
}): ModelFeatureMarkPayload {
  return {
    mark_code: args.code.trim(),
    feature_kind: args.kind.trim().toLowerCase(),
    source_ref: args.origin.trim(),
  }
}

export async function fetchModelFeatureMarks(): Promise<ModelFeatureMarkRow[]> {
  const reply = await fetch(PATH, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (!reply.ok) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się wczytać katalogu cechy modelu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ModelFeatureMarkRow[]
}

export async function saveModelFeatureMark(
  payload: ModelFeatureMarkPayload,
): Promise<ModelFeatureMarkRow> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "model-feature-mark-hitl",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status !== 201) {
    throw new ApiError(
      await readApiDetail(reply, "Nie udało się zapisać znacznika cechy modelu"),
      httpErrorStatus(reply),
    )
  }
  return (await reply.json()) as ModelFeatureMarkRow
}
