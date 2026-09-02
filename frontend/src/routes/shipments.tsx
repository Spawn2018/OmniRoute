import { createFileRoute } from "@tanstack/react-router"
import { ShipmentPage } from "@/features/shipment/catalog-page"

export const Route = createFileRoute("/shipments")({
  component: ShipmentPage,
})
