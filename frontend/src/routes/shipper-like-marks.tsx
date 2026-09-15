import { createFileRoute } from "@tanstack/react-router"
import { ShipperLikeMarkDesk } from "@/features/shipper-like-mark/catalog-page"

export const Route = createFileRoute("/shipper-like-marks")({
  component: ShipperLikeMarkDesk,
})
