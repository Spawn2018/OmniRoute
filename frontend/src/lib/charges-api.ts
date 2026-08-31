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
}

export function chargeCreateBody(args: {
  chargeCode: string
  buyAmount: string
  sellAmount: string
  currency: string
  rateLineId: string
}): {
  charge_code: string
  buy_amount: string
  buy_currency: string
  sell_amount: string
  sell_currency: string
  rate_line_id: string | null
} {
  const currency = args.currency.trim().toUpperCase()
  const linked = args.rateLineId.trim()
  return {
    charge_code: args.chargeCode.trim(),
    buy_amount: args.buyAmount.trim(),
    buy_currency: currency,
    sell_amount: args.sellAmount.trim(),
    sell_currency: currency,
    rate_line_id: linked === "" ? null : linked,
  }
}

async function readCharge(response: Response, fallback: string): Promise<Charge> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
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
}): Promise<Charge> {
  const response = await fetch("/api/v1/charges", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readCharge(response, "Błąd zapisu opłaty")
}
