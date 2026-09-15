import { createFileRoute } from "@tanstack/react-router"
import { ShipperAwardMarkDesk } from "@/features/shipper-award-mark/catalog-page"

export const Route = createFileRoute("/shipper-award-marks")({
  component: ShipperAwardMarkDesk,
})
