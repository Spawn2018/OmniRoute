import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const FIXTURE_PATH = "/api/v1/visibility-connectors"

export type VisibilityFixtureRow = {
  id: string
  organization_id: string
  connector_code: string
  system_kind: string
  source_ref: string
}

export type VisibilityFixtureBody = {
  connector_code: string
  system_kind: string
  source_ref: string
}

export function visibilityFixtureBody(draft: {
  deskSlug: string
  vendorToken: string
  originPointer: string
}): VisibilityFixtureBody {
  return {
    connector_code: draft.deskSlug.trim(),
    system_kind: draft.vendorToken.trim(),
    source_ref: draft.originPointer.trim(),
  }
}

async function readVisibilityJson<T>(response: Response, fallback: string, ok: number): Promise<T> {
  if (response.status === ok) {
    return (await response.json()) as T
  }
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function listVisibilityFixtures(): Promise<VisibilityFixtureRow[]> {
  const listed = await fetch(FIXTURE_PATH, { headers: requireAuthHeaders() })
  return readVisibilityJson(listed, "Błąd listy konektorów widoczności", 200)
}

export async function persistVisibilityConnector(
  payload: VisibilityFixtureBody,
): Promise<VisibilityFixtureRow> {
  const posted = await fetch(FIXTURE_PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  return readVisibilityJson(posted, "Błąd zapisu konektora widoczności", 201)
}
