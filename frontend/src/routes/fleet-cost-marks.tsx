import { createFileRoute } from "@tanstack/react-router"
import { FleetCostDesk } from "@/features/fleet-cost-mark/catalog-page"

export const Route = createFileRoute("/fleet-cost-marks")({
  component: FleetCostDesk,
})
