import { createFileRoute } from "@tanstack/react-router"
import { CostAllocationMarkDesk } from "@/features/cost-allocation-mark/catalog-page"

export const Route = createFileRoute("/cost-allocation-marks")({
  component: CostAllocationMarkDesk,
})
