import { createFileRoute } from "@tanstack/react-router"
import { ShipperTenderMarkDesk } from "@/features/shipper-tender-mark/catalog-page"

export const Route = createFileRoute("/shipper-tender-marks")({
  component: ShipperTenderMarkDesk,
})
