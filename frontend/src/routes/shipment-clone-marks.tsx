import { createFileRoute } from "@tanstack/react-router"
import { ShipmentCloneMarkDesk } from "@/features/shipment-clone-mark/catalog-page"

export const Route = createFileRoute("/shipment-clone-marks")({
  component: ShipmentCloneMarkDesk,
})
