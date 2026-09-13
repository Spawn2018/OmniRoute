import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TwinKindRow = {
  id: string
  organization_id: string
  kind_code: string
  source_ref: string
}

export type TwinKindPayload = {
  kind_code: string
  source_ref: string
}

const ENDPOINT = "/api/v1/twin-kinds" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeTwinKindPayload(draft: {
  kindCode: string
  sourceRef: string
}): TwinKindPayload {
  return {
    kind_code: draft.kindCode.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadTwinKinds(): Promise<TwinKindRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog rodzaju bliźniaka niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as TwinKindRow[]
}

export async function createTwinKind(payload: TwinKindPayload): Promise<TwinKindRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "twin-kind-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis rodzaju bliźniaka odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as TwinKindRow
}
