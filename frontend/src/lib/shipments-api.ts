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
  guide_code: string | null
  plant_label: string | null
  carrier_label: string | null
  asn_id: string | null
  is_waste: boolean
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
  guide_code?: string | null
  plant_label?: string | null
  carrier_label?: string | null
  is_waste?: boolean | null
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
