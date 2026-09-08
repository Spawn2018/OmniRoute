import { createFileRoute } from "@tanstack/react-router"
import { ParcelDesk } from "@/features/shipment-package/catalog-page"

export const Route = createFileRoute("/shipment-packages")({
  component: ParcelDesk,
})
