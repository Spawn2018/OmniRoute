import { createFileRoute } from "@tanstack/react-router"
import { TripBillMarkDesk } from "@/features/trip-bill-mark/catalog-page"

export const Route = createFileRoute("/trip-bill-marks")({
  component: TripBillMarkDesk,
})
