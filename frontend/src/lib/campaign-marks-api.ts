import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/campaign-marks"

export type CampaignMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  campaign_kind: string
  source_ref: string
}

export type CampaignMarkWrite = {
  mark_code: string
  campaign_kind: string
  source_ref: string
}

export function buildCampaignMarkWrite(fields: {
  code: string
  kind: string
  origin: string
}): CampaignMarkWrite {
  return {
    mark_code: fields.code.trim(),
    campaign_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchCampaignMarks(): Promise<CampaignMarkRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy znaczników kampanii", 200)
}

export async function saveCampaignMark(body: CampaignMarkWrite): Promise<CampaignMarkRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu znacznika kampanii", 201)
}
