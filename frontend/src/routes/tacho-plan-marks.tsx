import { createFileRoute } from "@tanstack/react-router"
import { TachoPlanMarkDesk } from "@/features/tacho-plan-mark/catalog-page"

export const Route = createFileRoute("/tacho-plan-marks")({
  component: TachoPlanMarkDesk,
})
