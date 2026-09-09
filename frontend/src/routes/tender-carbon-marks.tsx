import { createFileRoute } from "@tanstack/react-router"
import { CarbonDesk } from "@/features/tender-carbon-mark/catalog-page"

export const Route = createFileRoute("/tender-carbon-marks")({
  component: CarbonDesk,
})
