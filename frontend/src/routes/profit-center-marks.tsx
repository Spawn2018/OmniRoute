import { createFileRoute } from "@tanstack/react-router"
import { ProfitCenterMarkBoard } from "@/features/profit-center-mark/catalog-page"

export const Route = createFileRoute("/profit-center-marks")({
  component: ProfitCenterMarkBoard,
})
