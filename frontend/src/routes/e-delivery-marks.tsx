import { createFileRoute } from "@tanstack/react-router"
import { EDeliveryDesk } from "@/features/e-delivery-mark/catalog-page"

export const Route = createFileRoute("/e-delivery-marks")({
  component: EDeliveryDesk,
})
