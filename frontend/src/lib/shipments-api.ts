import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Shipment = {
  id: string
  organization_id: string
  quotation_id: string
  party_id: string
  source_ref: string
  shipment_ref: string | null
  parent_shipment_id: string | null
  relation_kind: string | null
  status: string
}

export async function fetchShipments(): Promise<Shipment[]> {
  const response = await fetch("/api/v1/shipments", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy zleceń"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as Shipment[]
}

export async function createShipment(input: {
  quotation_id: string
  source_ref: string
  shipment_ref?: string | null
  parent_shipment_id?: string | null
  relation_kind?: string | null
}): Promise<Shipment> {
  const response = await fetch("/api/v1/shipments", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu zlecenia"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as Shipment
}
