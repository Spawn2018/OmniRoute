import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ShipmentStakeholderRow = {
  id: string
  organization_id: string
  shipment_id: string
  party_id: string
  role: string
  source_ref: string
  superseded_by: string | null
}

const PATH = "/api/v1/shipment-stakeholders"

export function shipmentStakeholderBody(args: {
  shipmentId: string
  partyId: string
  role: string
}): { shipment_id: string; party_id: string; role: string; source_ref: string } {
  return {
    shipment_id: args.shipmentId.trim(),
    party_id: args.partyId.trim(),
    role: args.role.trim(),
    source_ref: "tenant:manual",
  }
}

export async function fetchShipmentStakeholders(shipmentId: string): Promise<ShipmentStakeholderRow[]> {
  const query = new URLSearchParams({ shipment_id: shipmentId })
  const reply = await fetch(`${PATH}?${query}`, { headers: requireAuthHeaders() })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd listy stron zlecenia"), httpErrorStatus(reply))
  }
  return (await reply.json()) as ShipmentStakeholderRow[]
}

export async function saveShipmentStakeholder(payload: {
  shipment_id: string
  party_id: string
  role: string
  source_ref: string
}): Promise<ShipmentStakeholderRow> {
  const headers = new Headers(requireAuthHeaders())
  headers.set("Accept", "application/json")
  headers.set("Content-Type", "application/json")
  const reply = await fetch(PATH, { method: "POST", headers, body: JSON.stringify(payload) })
  if (!reply.ok) {
    throw new ApiError(await readApiDetail(reply, "Błąd zapisu strony zlecenia"), httpErrorStatus(reply))
  }
  return (await reply.json()) as ShipmentStakeholderRow
}
