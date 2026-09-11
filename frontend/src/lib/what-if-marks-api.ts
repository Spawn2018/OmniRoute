import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/what-if-marks" as const

export type WhatIfMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  scenario_kind: string
  source_ref: string
}

export type WhatIfMarkDraft = {
  mark_code: string
  scenario_kind: string
  source_ref: string
}

export function draftWhatIfMark(fields: {
  mark: string
  scenario: string
  ref: string
}): WhatIfMarkDraft {
  return {
    mark_code: fields.mark.trim(),
    scenario_kind: fields.scenario.trim().toLowerCase(),
    source_ref: fields.ref.trim(),
  }
}

async function readOk<T>(response: Response, label: string, code: number): Promise<T> {
  if (response.status !== code) {
    throw new ApiError(await readApiDetail(response, label), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchWhatIfMarks(): Promise<WhatIfMarkRow[]> {
  const response = await fetch(PATH, { headers: requireAuthHeaders() })
  return readOk(response, "Lista what-if niedostępna", 200)
}

export async function postWhatIfMark(draft: WhatIfMarkDraft): Promise<WhatIfMarkRow> {
  const response = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(draft),
  })
  return readOk(response, "Zapis what-if nieudany", 201)
}
