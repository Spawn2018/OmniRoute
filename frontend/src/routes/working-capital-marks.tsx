import { createFileRoute } from "@tanstack/react-router"
import { WorkingCapitalMarkDesk } from "@/features/working-capital-mark/catalog-page"

export const Route = createFileRoute("/working-capital-marks")({
  component: WorkingCapitalMarkDesk,
})
