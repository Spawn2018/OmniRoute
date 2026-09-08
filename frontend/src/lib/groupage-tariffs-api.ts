import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const PATH = "/api/v1/groupage-tariffs"

export type WeightBand = {
  id: string
  organization_id: string
  location_id: string
  tariff_code: string
  chargeable_weight: string
  amount: string
  currency: string
  source_ref: string
}

export type WeightBandWrite = {
  location_id: string
  tariff_code: string
  chargeable_weight: string
  amount: string
  currency: string
  source_ref: string
}

export function bandWrite(args: {
  zoneToken: string
  bandToken: string
  massMark: string
  cashMark: string
  ccyMark: string
  originStamp: string
}): WeightBandWrite {
  return {
    location_id: args.zoneToken.trim(),
    tariff_code: args.bandToken.trim(),
    chargeable_weight: args.massMark.trim(),
    amount: args.cashMark.trim(),
    currency: args.ccyMark.trim().toUpperCase(),
    source_ref: args.originStamp.trim(),
  }
}

export async function listWeightBands(): Promise<WeightBand[]> {
  const reply = await fetch(PATH, { headers: requireAuthHeaders() })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy cennika drobnicy"), httpErrorStatus(reply))
  }
  const payload: unknown = await reply.json()
  return payload as WeightBand[]
}

export async function persistWeightBand(payload: WeightBandWrite): Promise<WeightBand> {
  const reply = await fetch(PATH, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      "Content-Type": "application/json",
      "X-Omni-Surface": "weight-band",
    },
    body: JSON.stringify(payload),
  })
  if (reply.status >= 400) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu cennika drobnicy"), httpErrorStatus(reply))
  }
  const saved: unknown = await reply.json()
  return saved as WeightBand
}
