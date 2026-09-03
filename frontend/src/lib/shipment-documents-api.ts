import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ShipmentDocument = {
  id: string
  organization_id: string
  shipment_id: string
  document_kind: string
  source_ref: string
}

export async function fetchShipmentDocuments(): Promise<ShipmentDocument[]> {
  const response = await fetch("/api/v1/shipment-documents", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy dokumentów zlecenia"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ShipmentDocument[]
}

export async function createShipmentDocument(input: {
  shipment_id: string
  document_kind: string
  source_ref: string
}): Promise<ShipmentDocument> {
  const response = await fetch("/api/v1/shipment-documents", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu dokumentu zlecenia"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as ShipmentDocument
}
