import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PartnerExchangeMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  exchange_kind: string
  source_ref: string
}

export type PartnerExchangePayload = {
  mark_code: string
  exchange_kind: string
  source_ref: string
}

const ROUTE = "/api/v1/partner-exchange-marks"

export function makePartnerExchangePayload(
  code: string,
  kind: string,
  ref: string,
): PartnerExchangePayload {
  return {
    mark_code: code.trim(),
    exchange_kind: kind.trim().toLowerCase(),
    source_ref: ref.trim(),
  }
}

export async function loadPartnerExchangeMarks(): Promise<PartnerExchangeMarkRow[]> {
  const answer = await fetch(ROUTE, { headers: requireAuthHeaders() })
  if (answer.ok) {
    return (await answer.json()) as PartnerExchangeMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(answer, "Lista znacznikow gieldy partnerskiej niedostepna"),
    httpErrorStatus(answer),
  )
}

export async function createPartnerExchangeMark(
  payload: PartnerExchangePayload,
): Promise<PartnerExchangeMarkRow> {
  const answer = await fetch(ROUTE, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (answer.status === 201) {
    return (await answer.json()) as PartnerExchangeMarkRow
  }
  throw new ApiError(
    await readApiDetail(answer, "Zapis znacznika gieldy partnerskiej nieudany"),
    httpErrorStatus(answer),
  )
}
