import { createFileRoute } from "@tanstack/react-router"
import { FleetPage } from "@/features/shipment/fleet-page"

export const Route = createFileRoute("/fleet")({
  component: FleetPage,
})
