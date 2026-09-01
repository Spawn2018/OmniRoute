import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Quotation = {
  id: string
  organization_id: string
  charge_code: string
  rate_line_id: string
  amount: string
  currency: string
  source_ref: string
  origin_port_id: string | null
  destination_port_id: string | null
  party_id: string | null
}

export type QuotationCreateBody = {
  charge_code: string
  origin_port_id: string
  destination_port_id: string
  party_id: string
}

export type QuotationListFilters = {
  partyId: string
  originPortId: string
  destinationPortId: string
}

export function quotationCreateBody(args: {
  chargeCode: string
  originPortId: string
  destinationPortId: string
  partyId: string
}): QuotationCreateBody {
  return {
    charge_code: args.chargeCode.trim(),
    origin_port_id: args.originPortId,
    destination_port_id: args.destinationPortId,
    party_id: args.partyId,
  }
}

async function readQuotation(response: Response, fallback: string): Promise<Quotation> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as Quotation
}

export async function fetchQuotations(filters: QuotationListFilters): Promise<Quotation[]> {
  const params = new URLSearchParams()
  if (filters.partyId !== "") {
    params.set("party_id", filters.partyId)
  }
  if (filters.originPortId !== "") {
    params.set("origin_port_id", filters.originPortId)
  }
  if (filters.destinationPortId !== "") {
    params.set("destination_port_id", filters.destinationPortId)
  }
  const query = params.toString() === "" ? "" : `?${params.toString()}`
  const response = await fetch(`/api/v1/quotations${query}`, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy wycen"), httpErrorStatus(response))
  }
  return (await response.json()) as Quotation[]
}

export async function createQuotation(body: QuotationCreateBody): Promise<Quotation> {
  const response = await fetch("/api/v1/quotations", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readQuotation(response, "Błąd wyceny")
}
