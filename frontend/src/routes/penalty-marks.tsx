import { createFileRoute } from "@tanstack/react-router"
import { PenaltyMarkDesk } from "@/features/penalty-mark/catalog-page"

export const Route = createFileRoute("/penalty-marks")({
  component: PenaltyMarkDesk,
})
