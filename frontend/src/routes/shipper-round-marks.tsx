import { createFileRoute } from "@tanstack/react-router"
import { ShipperRoundMarkDesk } from "@/features/shipper-round-mark/catalog-page"

export const Route = createFileRoute("/shipper-round-marks")({
  component: ShipperRoundMarkDesk,
})
