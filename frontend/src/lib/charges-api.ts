import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Charge = {
  id: string
  organization_id: string
  charge_code: string
  buy_amount: string
  buy_currency: string
  sell_amount: string
  sell_currency: string
  margin_amount: string
  margin_currency: string
  rate_line_id: string | null
  source_ref: string | null
}

export type CashFlowLeg = {
  id: string
  charge_code: string
  outflow_amount: string
  outflow_currency: string
  inflow_amount: string
  inflow_currency: string
}

export function cashFlowLegs<
  Row extends {
    id: string
    charge_code: string
    buy_amount: string
    buy_currency: string
    sell_amount: string
    sell_currency: string
  },
>(charges: readonly Row[]): CashFlowLeg[] {
  return charges.map((charge) => ({
    id: charge.id,
    charge_code: charge.charge_code,
    outflow_amount: charge.buy_amount,
    outflow_currency: charge.buy_currency,
    inflow_amount: charge.sell_amount,
    inflow_currency: charge.sell_currency,
  }))
}

export type BookkeepingLine = {
  id: string
  charge_code: string
  code_name: string
  buy_amount: string
  buy_currency: string
  sell_amount: string
  sell_currency: string
}

export function bookkeepingLines<
  ChargeRow extends {
    id: string
    charge_code: string
    buy_amount: string
    buy_currency: string
    sell_amount: string
    sell_currency: string
  },
  CodeRow extends { code: string; name: string },
>(charges: readonly ChargeRow[], codes: readonly CodeRow[]): BookkeepingLine[] {
  const names = new Map(codes.map((row) => [row.code, row.name]))
  return charges.map((charge) => ({
    id: charge.id,
    charge_code: charge.charge_code,
    code_name: names.get(charge.charge_code) ?? "",
    buy_amount: charge.buy_amount,
    buy_currency: charge.buy_currency,
    sell_amount: charge.sell_amount,
    sell_currency: charge.sell_currency,
  }))
}

export function comparisonChargeBody(
  lane: { chargeCode: string; amount: string; currency: string },
  quote: { amount: string; currency: string },
): {
  charge_code: string
  buy_amount: string
  buy_currency: string
  sell_amount: string
  sell_currency: string
  rate_line_id: null
  source_ref: string
} {
  return {
    charge_code: lane.chargeCode.trim(),
    buy_amount: quote.amount.trim(),
    buy_currency: quote.currency.trim().toUpperCase(),
    sell_amount: lane.amount.trim(),
    sell_currency: lane.currency.trim().toUpperCase(),
    rate_line_id: null,
    source_ref: "tenant:manual:comparison",
  }
}

export function chargeCreateBody(args: {
  chargeCode: string
  buyAmount: string
  sellAmount: string
  currency: string
  rateLineId: string
  sourceRef: string
  originUnlocode?: string
  destinationUnlocode?: string
  floorDecisionId?: string
}): {
  charge_code: string
  buy_amount: string
  buy_currency: string
  sell_amount: string
  sell_currency: string
  rate_line_id: string | null
  source_ref: string
  origin_unlocode?: string
  destination_unlocode?: string
  floor_decision_id?: string
} {
  const currency = args.currency.trim().toUpperCase()
  const linked = args.rateLineId.trim()
  const origin = (args.originUnlocode ?? "").trim().toUpperCase()
  const destination = (args.destinationUnlocode ?? "").trim().toUpperCase()
  const decision = (args.floorDecisionId ?? "").trim()
  const body: {
    charge_code: string
    buy_amount: string
    buy_currency: string
    sell_amount: string
    sell_currency: string
    rate_line_id: string | null
    source_ref: string
    origin_unlocode?: string
    destination_unlocode?: string
    floor_decision_id?: string
  } = {
    charge_code: args.chargeCode.trim(),
    buy_amount: args.buyAmount.trim(),
    buy_currency: currency,
    sell_amount: args.sellAmount.trim(),
    sell_currency: currency,
    rate_line_id: linked === "" ? null : linked,
    source_ref: args.sourceRef.trim(),
  }
  if (origin !== "") {
    body.origin_unlocode = origin
  }
  if (destination !== "") {
    body.destination_unlocode = destination
  }
  if (decision !== "") {
    body.floor_decision_id = decision
  }
  return body
}

async function readCharge(response: Response, fallback: string): Promise<Charge> {
  if (!response.ok) {
    const payload: unknown = await response.json().catch(() => null)
    let detail = fallback
    let decisionId: string | null = null
    if (typeof payload === "object" && payload !== null) {
      if ("detail" in payload && typeof (payload as { detail: unknown }).detail === "string") {
        detail = (payload as { detail: string }).detail
      }
      if (
        "decision_id" in payload &&
        typeof (payload as { decision_id: unknown }).decision_id === "string"
      ) {
        decisionId = (payload as { decision_id: string }).decision_id
      }
    }
    const message =
      decisionId === null ? detail : `${detail} · decyzja S11: ${decisionId}`
    throw new ApiError(message, httpErrorStatus(response))
  }
  return (await response.json()) as Charge
}

export async function fetchCharges(): Promise<Charge[]> {
  const response = await fetch("/api/v1/charges", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy opłat"), httpErrorStatus(response))
  }
  return (await response.json()) as Charge[]
}

export async function createCharge(body: {
  charge_code: string
  buy_amount: string
  buy_currency: string
  sell_amount: string
  sell_currency: string
  rate_line_id: string | null
  source_ref: string
  origin_unlocode?: string
  destination_unlocode?: string
  floor_decision_id?: string
}): Promise<Charge> {
  const response = await fetch("/api/v1/charges", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readCharge(response, "Błąd zapisu opłaty")
}
