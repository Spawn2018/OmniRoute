import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type BidDecisionMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  decision_kind: string
  source_ref: string
}

export type BidDecisionMarkPayload = {
  mark_code: string
  decision_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/bid-decision-marks" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeBidDecisionMarkPayload(
  markCode: string,
  decisionKind: string,
  sourceRef: string,
): BidDecisionMarkPayload {
  return {
    mark_code: markCode.trim(),
    decision_kind: decisionKind.trim().toLowerCase(),
    source_ref: sourceRef.trim(),
  }
}

export async function loadBidDecisionMarks(): Promise<BidDecisionMarkRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog bid decision niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as BidDecisionMarkRow[]
}

export async function createBidDecisionMark(
  payload: BidDecisionMarkPayload,
): Promise<BidDecisionMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "bid-decision-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis znacznika bid decision odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as BidDecisionMarkRow
}
