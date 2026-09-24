import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type RateLine = {
  id: string
  organization_id: string
  charge_code: string
  amount: string
  currency: string
  source_ref: string
  allotment_teu: string | null
  spot_or_contract: string | null
  superseded_by: string | null
}

export function rateLineCreateBody(args: {
  chargeCode: string
  amount: string
  currency: string
  sourceRef: string
  allotmentTeu: string
  spotOrContract: string
}): {
  charge_code: string
  amount: string
  currency: string
  source_ref: string
  allotment_teu?: string
  spot_or_contract?: string
} {
  const body: {
    charge_code: string
    amount: string
    currency: string
    source_ref: string
    allotment_teu?: string
    spot_or_contract?: string
  } = {
    charge_code: args.chargeCode.trim(),
    amount: args.amount.trim(),
    currency: args.currency.trim().toUpperCase(),
    source_ref: args.sourceRef.trim(),
  }
  const teu = args.allotmentTeu.trim()
  if (teu !== "") {
    body.allotment_teu = teu
  }
  const deal = args.spotOrContract.trim()
  if (deal !== "") {
    body.spot_or_contract = deal
  }
  return body
}

export function rateLineSupersedeBody(args: {
  amount: string
  currency: string
  sourceRef: string
  allotmentTeu: string
  spotOrContract: string
}): {
  amount: string
  currency: string
  source_ref: string
  allotment_teu?: string
  spot_or_contract?: string
} {
  const body: {
    amount: string
    currency: string
    source_ref: string
    allotment_teu?: string
    spot_or_contract?: string
  } = {
    amount: args.amount.trim(),
    currency: args.currency.trim().toUpperCase(),
    source_ref: args.sourceRef.trim(),
  }
  const teu = args.allotmentTeu.trim()
  if (teu !== "") {
    body.allotment_teu = teu
  }
  const deal = args.spotOrContract.trim()
  if (deal !== "") {
    body.spot_or_contract = deal
  }
  return body
}

async function readRateLine(response: Response, fallback: string): Promise<RateLine> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as RateLine
}

export async function fetchRateLines(): Promise<RateLine[]> {
  const response = await fetch("/api/v1/rate-lines", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy stawek"), httpErrorStatus(response))
  }
  return (await response.json()) as RateLine[]
}

export async function createRateLine(body: {
  charge_code: string
  amount: string
  currency: string
  source_ref: string
  allotment_teu?: string
  spot_or_contract?: string
}): Promise<RateLine> {
  const response = await fetch("/api/v1/rate-lines", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readRateLine(response, "Błąd zapisu stawki")
}

export async function supersedeRateLine(
  rateLineId: string,
  body: {
    amount: string
    currency: string
    source_ref: string
    allotment_teu?: string
    spot_or_contract?: string
  },
): Promise<RateLine> {
  const response = await fetch(`/api/v1/rate-lines/${rateLineId}/supersede`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readRateLine(response, "Błąd zastąpienia stawki")
}
