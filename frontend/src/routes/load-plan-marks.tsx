import { createFileRoute } from "@tanstack/react-router"
import { LoadPlanMarkDesk } from "@/features/load-plan-mark/catalog-page"

export const Route = createFileRoute("/load-plan-marks")({
  component: LoadPlanMarkDesk,
})
