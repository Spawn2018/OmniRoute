import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const ENDPOINT = "/api/v1/routing-guide-matches"

export type RoutingGuideMatchRow = {
  id: string
  organization_id: string
  mark_code: string
  match_kind: string
  source_ref: string
}

export type MatchWriteBody = {
  mark_code: string
  match_kind: string
  source_ref: string
}

export function toMatchWrite(fields: {
  slug: string
  kind: string
  pointer: string
}): MatchWriteBody {
  return {
    mark_code: fields.slug.trim(),
    match_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.pointer.trim(),
  }
}

async function decodeJson<T>(
  response: Response,
  fail: string,
  ok: number,
): Promise<T> {
  if (response.status !== ok) {
    throw new ApiError(await readApiDetail(response, fail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function listRoutingGuideMatches(): Promise<RoutingGuideMatchRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  return decodeJson(response, "Błąd listy trybów dopasowania", 200)
}

export async function createRoutingGuideMatch(
  body: MatchWriteBody,
): Promise<RoutingGuideMatchRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return decodeJson(response, "Błąd zapisu trybu dopasowania", 201)
}
