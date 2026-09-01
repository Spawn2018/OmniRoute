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
  source_ref: string
}

export type ChannelQuoteDraft = {
  partyId: string
  originPortId: string
  destinationPortId: string
  quoteDate: string
  amount: string
  currency: string
}

export const EMPTY_QUOTE_DRAFT: ChannelQuoteDraft = {
  partyId: "",
  originPortId: "",
  destinationPortId: "",
  quoteDate: "",
  amount: "",
  currency: "",
}

export function channelQuoteCreateBody(draft: ChannelQuoteDraft): {
  party_id: string
  origin_port_id: string
  destination_port_id: string
  quote_date: string
  amount: string
  currency: string
} {
  return {
    party_id: draft.partyId.trim(),
    origin_port_id: draft.originPortId.trim(),
    destination_port_id: draft.destinationPortId.trim(),
    quote_date: draft.quoteDate,
    amount: draft.amount.trim(),
    currency: draft.currency.trim().toUpperCase(),
  }
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
}): Promise<ChannelQuote> {
  const params = new URLSearchParams({
    party_id: input.partyId,
    origin_port_id: input.originPortId,
    destination_port_id: input.destinationPortId,
    on_date: input.onDate,
  })
  const response = await fetch(`/api/v1/channel-quotes/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readQuote(response, "Brak oferty z kanału")
}
