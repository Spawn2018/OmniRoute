import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ChannelQuote = {
  id: string
  organization_id: string
  party_id: string
  origin_port_id: string
  destination_port_id: string
  quote_date: string
  amount: string
  currency: string
  transit_days: number | null
  transport_mode: string
  source_ref: string
  is_cheapest: boolean
  is_fastest_tt: boolean
}

export type ChannelQuoteDraft = {
  partyId: string
  originPortId: string
  destinationPortId: string
  quoteDate: string
  amount: string
  currency: string
  transitDays?: string
  transportMode?: string
}

export const EMPTY_QUOTE_DRAFT: ChannelQuoteDraft = {
  partyId: "",
  originPortId: "",
  destinationPortId: "",
  quoteDate: "",
  amount: "",
  currency: "",
  transportMode: "other",
}

export function channelQuoteCreateBody(draft: ChannelQuoteDraft): {
  party_id: string
  origin_port_id: string
  destination_port_id: string
  quote_date: string
  amount: string
  currency: string
  transit_days?: number
  transport_mode: string
} {
  const days = draft.transitDays?.trim() ?? ""
  const body: {
    party_id: string
    origin_port_id: string
    destination_port_id: string
    quote_date: string
    amount: string
    currency: string
    transit_days?: number
    transport_mode: string
  } = {
    party_id: draft.partyId.trim(),
    origin_port_id: draft.originPortId.trim(),
    destination_port_id: draft.destinationPortId.trim(),
    quote_date: draft.quoteDate,
    amount: draft.amount.trim(),
    currency: draft.currency.trim().toUpperCase(),
    transport_mode: (draft.transportMode ?? "").trim() || "other",
  }
  if (days !== "") {
    body.transit_days = Number(days)
  }
  return body
}

async function readQuote(response: Response, fallback: string): Promise<ChannelQuote> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as ChannelQuote
}

export async function fetchChannelQuotes(): Promise<ChannelQuote[]> {
  const response = await fetch("/api/v1/channel-quotes", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy ofert z kanału"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ChannelQuote[]
}

export async function createChannelQuote(
  body: ReturnType<typeof channelQuoteCreateBody>,
): Promise<ChannelQuote> {
  const response = await fetch("/api/v1/channel-quotes", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readQuote(response, "Błąd zapisu oferty z kanału")
}

export async function resolveChannelQuote(input: {
  partyId: string
  originPortId: string
  destinationPortId: string
  onDate: string
  transportMode?: string
}): Promise<ChannelQuote> {
  const params = new URLSearchParams({
    party_id: input.partyId,
    origin_port_id: input.originPortId,
    destination_port_id: input.destinationPortId,
    on_date: input.onDate,
  })
  if (input.transportMode !== undefined && input.transportMode.trim() !== "") {
    params.set("transport_mode", input.transportMode.trim())
  }
  const response = await fetch(`/api/v1/channel-quotes/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readQuote(response, "Brak oferty z kanału")
}
