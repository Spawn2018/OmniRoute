import { createFileRoute } from "@tanstack/react-router"
import { FerryBookingMarkDesk } from "@/features/ferry-booking-mark/catalog-page"

export const Route = createFileRoute("/ferry-booking-marks")({
  component: FerryBookingMarkDesk,
})
