import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CargoClaimRow = {
  id: string
  organization_id: string
  shipment_id: string
  claim_kind: string
  damage_code: string
  cmr_notice_window: string
  notice_due_at: string
  suit_due_at: string
  source_ref: string
}

const CLAIMS_PATH = "/api/v1/cargo-claims"

export async function listCargoClaims(): Promise<CargoClaimRow[]> {
  const auth = requireAuthHeaders()
  const reply = await fetch(CLAIMS_PATH, { headers: auth })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy reklamacji"), httpErrorStatus(reply))
  }
  return (await reply.json()) as CargoClaimRow[]
}

export async function saveCargoClaim(payload: {
  shipment_id: string
  claim_kind: string
  damage_code: string
  cmr_notice_window: string
  notice_due_at: string
  suit_due_at: string
  source_ref: string
}): Promise<CargoClaimRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(CLAIMS_PATH, {
    method: "POST",
    headers: new Headers({
      ...auth,
      Accept: "application/json",
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu reklamacji"), httpErrorStatus(reply))
  }
  return (await reply.json()) as CargoClaimRow
}
