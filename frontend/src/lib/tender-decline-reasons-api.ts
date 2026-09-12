import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type TenderDeclineReasonRow = {
  id: string
  organization_id: string
  mark_code: string
  decline_kind: string
  source_ref: string
}

export type TenderDeclineReasonPayload = {
  mark_code: string
  decline_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/tender-decline-reasons"

function trimPayload(
  markCode: string,
  declineKind: string,
  sourceRef: string,
): TenderDeclineReasonPayload {
  return {
    mark_code: markCode.trim(),
    decline_kind: declineKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export function makeTenderDeclineReasonPayload(
  markCode: string,
  declineKind: string,
  sourceRef: string,
): TenderDeclineReasonPayload {
  return trimPayload(markCode, declineKind, sourceRef)
}

async function raiseIfBad(response: Response, fallback: string): Promise<void> {
  if (response.ok) return
  throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
}

export async function loadTenderDeclineReasons(): Promise<TenderDeclineReasonRow[]> {
  const response = await fetch(ENDPOINT, { headers: requireAuthHeaders() })
  await raiseIfBad(response, "Lista powodow decline niedostepna")
  return (await response.json()) as TenderDeclineReasonRow[]
}

export async function createTenderDeclineReason(
  payload: TenderDeclineReasonPayload,
): Promise<TenderDeclineReasonRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    await raiseIfBad(response, "Zapis powodu decline nieudany")
  }
  return (await response.json()) as TenderDeclineReasonRow
}
