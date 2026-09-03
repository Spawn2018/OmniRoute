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
  customer_rfq_id: string | null
  commodity_code_id: string | null
  dangerous_good_id: string | null
  document_number: string | null
  negotiated_channel_quote_id: string | null
  noted_credit_review_id: string | null
}

export type QuotationDocumentLayout = {
  prefix: string | null
  print_template: string
}

export type QuotationCreateBody = {
  charge_code: string
  origin_port_id: string
  destination_port_id: string
  party_id: string
  customer_rfq_id?: string
  commodity_code_id?: string
  dangerous_good_id?: string
}

export type QuotationListFilters = {
  partyId: string
  originPortId: string
  destinationPortId: string
  customerRfqId?: string
}

export function quotationCreateBody(args: {
  chargeCode: string
  originPortId: string
  destinationPortId: string
  partyId: string
  customerRfqId?: string
  commodityCodeId?: string
  dangerousGoodId?: string
}): QuotationCreateBody {
  const body: QuotationCreateBody = {
    charge_code: args.chargeCode.trim(),
    origin_port_id: args.originPortId,
    destination_port_id: args.destinationPortId,
    party_id: args.partyId,
  }
  const rfqId = args.customerRfqId?.trim()
  if (rfqId) {
    body.customer_rfq_id = rfqId
  }
  const hsId = args.commodityCodeId?.trim()
  if (hsId) {
    body.commodity_code_id = hsId
  }
  const unId = args.dangerousGoodId?.trim()
  if (unId) {
    body.dangerous_good_id = unId
  }
  return body
}

export type QuotationBatchBody = {
  charge_codes: string[]
  origin_port_id: string
  destination_port_id: string
  party_id: string
  customer_rfq_id?: string
  commodity_code_id?: string
  dangerous_good_id?: string
}

export function quotationBatchBody(args: {
  chargeCodesText: string
  originPortId: string
  destinationPortId: string
  partyId: string
  customerRfqId?: string
  commodityCodeId?: string
  dangerousGoodId?: string
}): QuotationBatchBody {
  const charge_codes = args.chargeCodesText
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line !== "")
  const body: QuotationBatchBody = {
    charge_codes,
    origin_port_id: args.originPortId,
    destination_port_id: args.destinationPortId,
    party_id: args.partyId,
  }
  const rfqId = args.customerRfqId?.trim()
  if (rfqId) {
    body.customer_rfq_id = rfqId
  }
  const hsId = args.commodityCodeId?.trim()
  if (hsId) {
    body.commodity_code_id = hsId
  }
  const unId = args.dangerousGoodId?.trim()
  if (unId) {
    body.dangerous_good_id = unId
  }
  return body
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

export function quotationOperationalExceptions(rows: readonly Quotation[]): Quotation[] {
  const exceptions: Quotation[] = []
  for (const row of rows) {
    if (row.party_id === null) {
      continue
    }
    if (row.origin_port_id !== null && row.destination_port_id !== null) {
      continue
    }
    exceptions.push(row)
  }
  return exceptions
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

export function quotationAcceptancePending<
  Decision extends { subject_kind: string; subject_id: string; status: string },
>(rows: readonly Quotation[], decisions: readonly Decision[] = []): Quotation[] {
  const accepted = new Set<string>()
  for (const decision of decisions) {
    if (decision.subject_kind !== "quotation" || decision.status !== "accepted") {
      continue
    }
    accepted.add(decision.subject_id)
  }
  const pending: Quotation[] = []
  for (const row of rows) {
    if (row.party_id === null || accepted.has(row.id)) {
      continue
    }
    pending.push(row)
  }
  return pending
}

export function quotationCarrierInquiries<
  Quote extends {
    id: string
    party_id: string
    origin_port_id: string
    destination_port_id: string
  },
>(lanes: readonly QuotationLane[], quotes: readonly Quote[]): Quote[] {
  const keys = new Set(
    lanes.map((lane) => `${lane.partyId}:${lane.originPortId}:${lane.destinationPortId}`),
  )
  const matched: Quote[] = []
  const seen = new Set<string>()
  for (const quote of quotes) {
    const key = `${quote.party_id}:${quote.origin_port_id}:${quote.destination_port_id}`
    if (!keys.has(key) || seen.has(quote.id)) {
      continue
    }
    seen.add(quote.id)
    matched.push(quote)
  }
  return matched
}

export type ResponseComparison<
  Quote extends {
    id: string
    origin_port_id: string
    destination_port_id: string
  },
> = {
  originPortId: string
  destinationPortId: string
  quotations: QuotationLane[]
  quotes: Quote[]
}

export function quotationResponseComparisons<
  Quote extends {
    id: string
    origin_port_id: string
    destination_port_id: string
  },
>(lanes: readonly QuotationLane[], quotes: readonly Quote[]): ResponseComparison<Quote>[] {
  const lanesByPair = new Map<string, QuotationLane[]>()
  for (const lane of lanes) {
    const pair = `${lane.originPortId}:${lane.destinationPortId}`
    const group = lanesByPair.get(pair)
    if (group === undefined) {
      lanesByPair.set(pair, [lane])
      continue
    }
    group.push(lane)
  }
  const quotesByPair = new Map<string, Quote[]>()
  const seenQuote = new Set<string>()
  for (const quote of quotes) {
    if (seenQuote.has(quote.id)) {
      continue
    }
    seenQuote.add(quote.id)
    const pair = `${quote.origin_port_id}:${quote.destination_port_id}`
    const group = quotesByPair.get(pair)
    if (group === undefined) {
      quotesByPair.set(pair, [quote])
      continue
    }
    group.push(quote)
  }
  const rows: ResponseComparison<Quote>[] = []
  for (const [pair, quotations] of lanesByPair) {
    const matched = quotesByPair.get(pair)
    if (matched === undefined) {
      continue
    }
    const first = quotations[0]
    rows.push({
      originPortId: first.originPortId,
      destinationPortId: first.destinationPortId,
      quotations,
      quotes: matched,
    })
  }
  return rows
}

export type QuoteInvoiceSettlement<
  ChargeRow extends {
    id: string
    rate_line_id: string | null
  },
> = {
  rateLineId: string
  quotations: Quotation[]
  charges: ChargeRow[]
}

export function quotationInvoiceSettlements<
  ChargeRow extends {
    id: string
    rate_line_id: string | null
  },
>(rows: readonly Quotation[], charges: readonly ChargeRow[]): QuoteInvoiceSettlement<ChargeRow>[] {
  const quotationsByLine = new Map<string, Quotation[]>()
  for (const row of rows) {
    const group = quotationsByLine.get(row.rate_line_id)
    if (group === undefined) {
      quotationsByLine.set(row.rate_line_id, [row])
      continue
    }
    group.push(row)
  }
  const chargesByLine = new Map<string, ChargeRow[]>()
  const seenCharge = new Set<string>()
  for (const charge of charges) {
    if (charge.rate_line_id === null || seenCharge.has(charge.id)) {
      continue
    }
    seenCharge.add(charge.id)
    const group = chargesByLine.get(charge.rate_line_id)
    if (group === undefined) {
      chargesByLine.set(charge.rate_line_id, [charge])
      continue
    }
    group.push(charge)
  }
  const settlements: QuoteInvoiceSettlement<ChargeRow>[] = []
  for (const [rateLineId, quotations] of quotationsByLine) {
    const matched = chargesByLine.get(rateLineId)
    if (matched === undefined) {
      continue
    }
    settlements.push({ rateLineId, quotations, charges: matched })
  }
  return settlements
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
  if (filters.customerRfqId !== undefined && filters.customerRfqId !== "") {
    params.set("customer_rfq_id", filters.customerRfqId)
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

export async function fetchQuotationDocumentLayout(): Promise<QuotationDocumentLayout> {
  const response = await fetch("/api/v1/quotations/document-layout", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd szablonu dokumentu oferty"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as QuotationDocumentLayout
}

export async function issueQuotationDocumentNumber(quotationId: string): Promise<Quotation> {
  const response = await fetch(`/api/v1/quotations/${quotationId}/document-number`, {
    method: "POST",
    headers: requireAuthHeaders(),
  })
  return readQuotation(response, "Błąd nadania numeru oferty")
}

export async function noteQuotationRisk(
  quotationId: string,
  creditReviewId: string,
): Promise<Quotation> {
  const response = await fetch(`/api/v1/quotations/${quotationId}/note-risk`, {
    method: "PATCH",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ credit_review_id: creditReviewId }),
  })
  return readQuotation(response, "Błąd zapisu faktu ryzyka")
}

export async function negotiateQuotation(
  quotationId: string,
  channelQuoteId: string,
): Promise<Quotation> {
  const response = await fetch(`/api/v1/quotations/${quotationId}/negotiate`, {
    method: "PATCH",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ channel_quote_id: channelQuoteId }),
  })
  return readQuotation(response, "Błąd zapisu wyniku negocjacji")
}
