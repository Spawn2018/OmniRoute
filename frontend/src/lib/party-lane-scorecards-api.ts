import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PartyLaneScorecard = {
  id: string
  organization_id: string
  party_id: string
  origin_port_id: string
  destination_port_id: string
  window_days: number
  sample_size: number
  answered_inquiry_count: number
  shipment_count: number
  cheapest_count: number
  median_response_hours: string | null
  computed_at: string
  source_ref: string
  hint: string
}

export type LaneScorecardDraft = {
  partyId: string
  originPortId: string
  destinationPortId: string
  windowDays: string
  sampleSize: string
  answeredInquiryCount: string
  shipmentCount: string
  cheapestCount: string
  medianHours: string
}

export const EMPTY_LANE_DRAFT: LaneScorecardDraft = {
  partyId: "",
  originPortId: "",
  destinationPortId: "",
  windowDays: "90",
  sampleSize: "0",
  answeredInquiryCount: "0",
  shipmentCount: "0",
  cheapestCount: "0",
  medianHours: "",
}

function blankToNull(raw: string): string | null {
  const trimmed = raw.trim()
  return trimmed.length === 0 ? null : trimmed
}

function asCount(raw: string): number {
  const parsed = Number.parseInt(raw, 10)
  return Number.isInteger(parsed) ? parsed : 0
}

export function laneScorecardUpsertBody(draft: LaneScorecardDraft): {
  party_id: string
  origin_port_id: string
  destination_port_id: string
  window_days: number
  sample_size: number
  answered_inquiry_count: number
  shipment_count: number
  cheapest_count: number
  median_response_hours: string | null
} {
  return {
    party_id: draft.partyId.trim(),
    origin_port_id: draft.originPortId.trim(),
    destination_port_id: draft.destinationPortId.trim(),
    window_days: asCount(draft.windowDays) || 90,
    sample_size: asCount(draft.sampleSize),
    answered_inquiry_count: asCount(draft.answeredInquiryCount),
    shipment_count: asCount(draft.shipmentCount),
    cheapest_count: asCount(draft.cheapestCount),
    median_response_hours: blankToNull(draft.medianHours),
  }
}

async function readLane(response: Response, fallback: string): Promise<PartyLaneScorecard> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as PartyLaneScorecard
}

export async function fetchPartyLaneScorecards(): Promise<PartyLaneScorecard[]> {
  const response = await fetch("/api/v1/party-lane-scorecards", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy kart lane"), httpErrorStatus(response))
  }
  return (await response.json()) as PartyLaneScorecard[]
}

export async function upsertPartyLaneScorecard(
  body: ReturnType<typeof laneScorecardUpsertBody>,
): Promise<PartyLaneScorecard> {
  const response = await fetch("/api/v1/party-lane-scorecards", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readLane(response, "Błąd zapisu karty lane")
}
