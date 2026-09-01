import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type PartyScorecard = {
  id: string
  organization_id: string
  party_id: string
  response_rate: string | null
  median_response_hours: string | null
  price_position: string | null
  quote_invoice_match_rate: string | null
  rollover_count: number | null
  sample_size: number
  window_days: number
  computed_at: string
  source_ref: string
}

export type ScorecardDraft = {
  partyId: string
  responseRate: string
  medianHours: string
  pricePosition: string
  quoteInvoiceMatch: string
  rolloverCount: string
  sampleSize: string
  windowDays: string
}

export const EMPTY_SCORECARD_DRAFT: ScorecardDraft = {
  partyId: "",
  responseRate: "",
  medianHours: "",
  pricePosition: "",
  quoteInvoiceMatch: "",
  rolloverCount: "",
  sampleSize: "0",
  windowDays: "90",
}

function blankToNull(raw: string): string | null {
  const trimmed = raw.trim()
  return trimmed.length === 0 ? null : trimmed
}

export function scorecardUpsertBody(draft: ScorecardDraft): {
  response_rate: string | null
  median_response_hours: string | null
  price_position: string | null
  quote_invoice_match_rate: string | null
  rollover_count: number | null
  sample_size: number
  window_days: number
} {
  const rollover = draft.rolloverCount.trim()
  return {
    response_rate: blankToNull(draft.responseRate),
    median_response_hours: blankToNull(draft.medianHours),
    price_position: blankToNull(draft.pricePosition),
    quote_invoice_match_rate: blankToNull(draft.quoteInvoiceMatch),
    rollover_count: rollover.length === 0 ? null : Number.parseInt(rollover, 10),
    sample_size: Number.parseInt(draft.sampleSize, 10),
    window_days: Number.parseInt(draft.windowDays, 10),
  }
}

async function readScorecard(response: Response, fallback: string): Promise<PartyScorecard> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as PartyScorecard
}

export async function fetchPartyScorecards(): Promise<PartyScorecard[]> {
  const response = await fetch("/api/v1/party-scorecards", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy kart"), httpErrorStatus(response))
  }
  return (await response.json()) as PartyScorecard[]
}

export async function fetchPartyScorecard(partyId: string): Promise<PartyScorecard> {
  const response = await fetch(`/api/v1/party-scorecards/${partyId}`, {
    headers: requireAuthHeaders(),
  })
  return readScorecard(response, "Brak karty wyników")
}

export async function upsertPartyScorecard(
  partyId: string,
  body: ReturnType<typeof scorecardUpsertBody>,
): Promise<PartyScorecard> {
  const response = await fetch(`/api/v1/party-scorecards/${partyId}`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readScorecard(response, "Błąd zapisu karty")
}
