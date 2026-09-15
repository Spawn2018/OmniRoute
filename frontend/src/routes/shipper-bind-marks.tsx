import { createFileRoute } from "@tanstack/react-router"
import { ShipperBindMarkDesk } from "@/features/shipper-bind-mark/catalog-page"

export const Route = createFileRoute("/shipper-bind-marks")({
  component: ShipperBindMarkDesk,
})
