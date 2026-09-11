import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const GUIDE_PATH = "/api/v1/routing-guides"

export type RoutingGuideRow = {
  id: string
  organization_id: string
  guide_code: string
  lane_label: string | null
  mode_label: string | null
  source_ref: string
}

export type RoutingGuideBody = {
  guide_code: string
  lane_label: string | null
  mode_label: string | null
  source_ref: string
}

function optionalLabel(raw: string): string | null {
  const label = raw.trim()
  return label.length === 0 ? null : label
}

export function routingGuideBody(draft: {
  guideSlug: string
  laneText: string
  modeText: string
  originPointer: string
}): RoutingGuideBody {
  return {
    guide_code: draft.guideSlug.trim(),
    lane_label: optionalLabel(draft.laneText),
    mode_label: optionalLabel(draft.modeText),
    source_ref: draft.originPointer.trim(),
  }
}

async function readGuideJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listRoutingGuides(): Promise<RoutingGuideRow[]> {
  const listed = await fetch(GUIDE_PATH, { headers: requireAuthHeaders() })
  return readGuideJson(listed, "Błąd listy przewodników routingu", 200)
}

export async function persistRoutingGuide(payload: RoutingGuideBody): Promise<RoutingGuideRow> {
  const posted = await fetch(GUIDE_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readGuideJson(posted, "Błąd zapisu przewodnika routingu", 201)
}
