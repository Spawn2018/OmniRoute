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

export type QuotationBatchBody = {
  charge_codes: string[]
  origin_port_id: string
  destination_port_id: string
  party_id: string
}

export function quotationBatchBody(args: {
  chargeCodesText: string
  originPortId: string
  destinationPortId: string
  partyId: string
}): QuotationBatchBody {
  const charge_codes = args.chargeCodesText
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line !== "")
  return {
    charge_codes,
    origin_port_id: args.originPortId,
    destination_port_id: args.destinationPortId,
    party_id: args.partyId,
  }
}

export function quotationCurrencies(rows: readonly Quotation[]): string[] {
  return [...new Set(rows.map((row) => row.currency))].sort()
}

export function quotationSkipsNbpCatalog(currency: string): boolean {
  return currency.trim().toUpperCase() === "PLN"
}

export function quotationPartyIds(rows: readonly Quotation[]): string[] {
  const ids = new Set<string>()
  for (const row of rows) {
    if (row.party_id !== null) {
      ids.add(row.party_id)
    }
  }
  return [...ids].sort()
}

export type QuotationLane = {
  id: string
  chargeCode: string
  partyId: string
  originPortId: string
  destinationPortId: string
  amount: string
  currency: string
}

export function quotationLanes(rows: readonly Quotation[]): QuotationLane[] {
  const lanes: QuotationLane[] = []
  for (const row of rows) {
    if (row.party_id === null || row.origin_port_id === null || row.destination_port_id === null) {
      continue
    }
    lanes.push({
      id: row.id,
      chargeCode: row.charge_code,
      partyId: row.party_id,
      originPortId: row.origin_port_id,
      destinationPortId: row.destination_port_id,
      amount: row.amount,
      currency: row.currency,
    })
  }
  return lanes
}

export type CustomerInquiryTrail = {
  partyId: string
  quotations: Quotation[]
}

export function quotationInquiryTrails(rows: readonly Quotation[]): CustomerInquiryTrail[] {
  const byParty = new Map<string, Quotation[]>()
  for (const row of rows) {
    if (row.party_id === null) {
      continue
    }
    const group = byParty.get(row.party_id)
    if (group === undefined) {
      byParty.set(row.party_id, [row])
      continue
    }
    group.push(row)
  }
  return [...byParty.entries()]
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([partyId, quotations]) => ({ partyId, quotations }))
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

export async function createQuotationBatch(body: QuotationBatchBody): Promise<Quotation[]> {
  const response = await fetch("/api/v1/quotations/batch", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd wyceny wsadowej"), httpErrorStatus(response))
  }
  return (await response.json()) as Quotation[]
}
