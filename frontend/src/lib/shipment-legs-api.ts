import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ShipmentLegRow = {
  id: string
  organization_id: string
  shipment_id: string
  origin_location_id: string
  destination_location_id: string
  leg_kind: string
  source_ref: string
}

const LEGS_PATH = "/api/v1/shipment-legs"

export async function listShipmentLegs(): Promise<ShipmentLegRow[]> {
  const auth = requireAuthHeaders()
  const reply = await fetch(LEGS_PATH, { headers: auth })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy odcinków"), httpErrorStatus(reply))
  }
  return (await reply.json()) as ShipmentLegRow[]
}

export async function saveShipmentLeg(payload: {
  shipment_id: string
  origin_location_id: string
  destination_location_id: string
  source_ref: string
}): Promise<ShipmentLegRow> {
  const auth = requireAuthHeaders()
  const reply = await fetch(LEGS_PATH, {
    method: "POST",
    headers: new Headers({
      ...auth,
      Accept: "application/json",
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu odcinka"), httpErrorStatus(reply))
  }
  return (await reply.json()) as ShipmentLegRow
}
