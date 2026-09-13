import { createFileRoute } from "@tanstack/react-router"
import { RoutePlanMarkDesk } from "@/features/route-plan-mark/catalog-page"

export const Route = createFileRoute("/route-plan-marks")({
  component: RoutePlanMarkDesk,
})
