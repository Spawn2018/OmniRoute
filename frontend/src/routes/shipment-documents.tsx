import { createFileRoute } from "@tanstack/react-router"
import { ShipmentDocumentPage } from "@/features/shipment-document/catalog-page"

export const Route = createFileRoute("/shipment-documents")({
  component: ShipmentDocumentPage,
})
